from ._anvil_designer import FilterBarTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil import *
import anvil.media
from anvil import *

DISPLAY_LIMIT = 10        # 弹窗最多显示的选项数

class FilterBar(FlowPanel):
    """
  rows       : 全量数据 (list of dict / DataRow)
  on_search  : 回调函数(filtered_rows)。若未提供，则抛事件 'x-search'
  """
    def __init__(self, rows, on_search=None, **properties):
        super().__init__(**properties)
        self.all_rows  = rows or []
        self.on_search = on_search
        self.filter_set = {}           # {field:set(values)}
        self.inputs     = {}
        self.dist_cache = {}           # {field: (preview_list, total_cnt)}
        self.role    = 'filter-bar'
        self.spacing = 'none'

        if not self.all_rows:
            return

        # 字段列表
        self.fields = list(dict(self.all_rows[0]).keys())

        # 输入框
        for f in self.fields:
            tb = TextBox(placeholder=str(f), width=140)
            tb.tag.field = f
            tb.set_event_handler('focus', self._open_selector)
            self.add_component(tb)
            self.inputs[f]       = tb
            self.filter_set[f]   = set()

        # 搜索、导出按钮
        btn_search = Button(text='搜索', icon='fa:search', role='primary')
        btn_down   = Button(text='导出CSV', icon='fa:download')
        btn_search.set_event_handler('click', self._do_search)
        btn_down.set_event_handler('click',  self._do_export)
        self.add_component(btn_search)
        self.add_component(btn_down)

    # ────────────────────────────────
    #  懒加载 distinct，且最多收集 DISPLAY_LIMIT 条用于显示
    # ────────────────────────────────
    def _get_preview_values(self, field):
        if field in self.dist_cache:
            return self.dist_cache[field]

        seen, preview = set(), []
        for r in self.all_rows:
            val = dict(r).get(field)
            if val is None:
                continue
            sval = str(val)
            if sval not in seen:
                seen.add(sval)
                if len(preview) < DISPLAY_LIMIT:
                    preview.append(sval)
        total_cnt = len(seen)
        preview.sort()
        self.dist_cache[field] = (preview, total_cnt)
        return self.dist_cache[field]

    # ────────────────────────────────
    #  弹出选择/输入
    # ────────────────────────────────
    def _open_selector(self, **e):
        tb, field = e['sender'], e['sender'].tag.field
        preview_vals, total_cnt = self._get_preview_values(field)

        manual = TextBox(placeholder='手动输入，逗号分隔', width='100%')
        checks = ColumnPanel()
        for v in preview_vals:
            cb = CheckBox(text=v)
            cb.checked = v in self.filter_set[field]
            checks.add_component(cb)

        if total_cnt > DISPLAY_LIMIT:
            checks.add_component(
                Label(text=f"...共 {total_cnt} 条，仅显示前 {DISPLAY_LIMIT} 条，请手动输入筛选", italic=True)
            )

        # 全选 / 清空
        def mark(flag):
            for c in checks.get_components():
                if isinstance(c, CheckBox):
                    c.checked = flag

        btn_all  = Button(text='全选',  width='48%', role='primary')
        btn_none = Button(text='清空',  width='48%')
        btn_all.set_event_handler('click',  lambda **k: mark(True))
        btn_none.set_event_handler('click', lambda **k: mark(False))
        fp_btns = FlowPanel(spacing='small')
        fp_btns.add_component(btn_all)
        fp_btns.add_component(btn_none)

        layout = ColumnPanel()
        layout.add_component(manual)
        layout.add_component(fp_btns)
        layout.add_component(checks)

        if not alert(layout, title=f"选择 / 输入  {field}",
                     buttons=[('确定', True), ('取消', False)]):
            return

        selected = {c.text for c in checks.get_components()
                    if isinstance(c, CheckBox) and c.checked}
        if manual.text:
            selected.update(s.strip() for s in manual.text.split(',') if s.strip())

        self.filter_set[field] = selected
        tb.text = ', '.join(selected)

    # ────────────────────────────────
    #  执行过滤
    # ────────────────────────────────
    def _apply_filter(self):
        def match(row):
            rd = dict(row)
            for f, vals in self.filter_set.items():
                if not vals:
                    continue
                cell = str(rd.get(f, ""))
                if not any(v in cell for v in vals):
                    return False
            return True
        return [r for r in self.all_rows if match(r)]

    # ────────────────────────────────
    #  搜索按钮
    # ────────────────────────────────
    def _do_search(self, **e):
        self._emit_rows(self._apply_filter())

    # ────────────────────────────────
    #  导出按钮
    # ────────────────────────────────
    def _do_export(self, **e):
        rows = self._apply_filter()
        if not rows:
            alert("无可导出的数据！")
            return

        fields = self.fields
        # 构造 CSV 字符串
        def esc(x):
            s = str(x)
            if any(c in s for c in (',', '"', '\n')):
                s = '"' + s.replace('"', '""') + '"'
            return s
        lines = [",".join(fields)]
        for r in rows:
            rd = dict(r)
            lines.append(",".join(esc(rd.get(f, "")) for f in fields))

        data = "\n".join(lines)
        csv_bytes = ("\ufeff" + data).encode("utf-8")   # 前置 UTF-8 BOM

        media = anvil.BlobMedia("text/plain", csv_bytes, "export.csv")
        anvil.media.download(media)

    # ────────────────────────────────
    #  抛结果
    # ────────────────────────────────
    def _emit_rows(self, rows):
        if self.on_search:
            self.on_search(rows)
        else:
            self.raise_event('x-search', rows=rows)
