from ._anvil_designer import FilterBarTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil import *
import anvil.media

DISPLAY_LIMIT = 10      # 弹窗最多显示多少个值

class FilterBar(FlowPanel):
    def __init__(self, rows, on_search=None, **properties):
        super().__init__(**properties)
        self.all_rows   = rows or []
        self.on_search  = on_search
        self.filter_set = {}            # {field:set(values)}
        self.inputs     = {}
        self.spacing    = 'none'
        self.role       = 'filter-bar'

        if not self.all_rows:
            return

        # 预计算 distinct
        self.distinct = {
            k: sorted({str(dict(r).get(k, "")) for r in self.all_rows
                       if dict(r).get(k) is not None})
            for k in dict(self.all_rows[0]).keys()
        }

        # 输入框
        for field in self.distinct:
            tb = TextBox(placeholder=str(field), width=140,)
            tb.tag.field = field
            tb.set_event_handler('focus', self._open_selector)
            self.add_component(tb)
            self.inputs[field]   = tb
            self.filter_set[field] = set()

        # 搜索与导出
        btn_search = Button(text='搜索', icon='fa:search', role='primary')
        btn_dl     = Button(text='导出CSV', icon='fa:download')
        btn_search.set_event_handler('click', self._do_search)
        btn_dl.set_event_handler('click', self._export_csv)
        self.add_component(btn_search)
        self.add_component(btn_dl)

    # ---------------- 弹窗选择 ----------------
    def _open_selector(self, **e):
        tb, field = e['sender'], e['sender'].tag.field
        values = self.distinct[field]
        preview = values[:DISPLAY_LIMIT]

        manual = TextBox(placeholder='手动输入，逗号分隔', width='100%')
        checks = ColumnPanel()
        for v in preview:
            cb = CheckBox(text=v)
            cb.checked = v in self.filter_set[field]
            checks.add_component(cb)

        if len(values) > DISPLAY_LIMIT:
            checks.add_component(Label(text=f"... 共 {len(values)} 条，仅显示前 {DISPLAY_LIMIT} 条，"
                                       f"如未出现请手动输入"))

        # 全选 / 清空
        def mark(all_on):
            for c in checks.get_components():
                if isinstance(c, CheckBox):
                    c.checked = all_on
        btn_all  = Button(text='全选', width='48%', role='primary')
        btn_none = Button(text='清空', width='48%')
        btn_all.set_event_handler('click',  lambda **k: mark(True))
        btn_none.set_event_handler('click', lambda **k: mark(False))
        fp_btns = FlowPanel(spacing='small')
        fp_btns.add_component(btn_all)
        fp_btns.add_component(btn_none)

        lay = ColumnPanel()
        lay.add_component(manual)
        lay.add_component(fp_btns)
        lay.add_component(checks)

        if not alert(lay, title=f"选择 / 输入  {field}",
                     buttons=[('确定', True), ('取消', False)]):
            return

        chosen = {c.text for c in checks.get_components()
                  if isinstance(c, CheckBox) and c.checked}
        if manual.text:
            chosen.update(x.strip() for x in manual.text.split(',') if x.strip())
        self.filter_set[field] = chosen
        tb.text = ', '.join(chosen)

    # ---------------- 搜索 ----------------
    def _do_search(self, **e):
        rows = self._apply_filter()
        self._emit_rows(rows)

    # ---------------- 导出 CSV ----------------
    def _export_csv(self, **e):
        rows = self._apply_filter()
        if not rows:
            alert("无可导出的数据!");  return

        fields = list(dict(self.all_rows[0]).keys())
        # 拼 CSV 字符串（不依赖 csv 库）
        lines = [",".join(fields)]
        for r in rows:
            rd = dict(r)
            # 简单转义：把包含逗号/引号的字段用双引号包裹并替换内部引号
            def esc(x):
                s = str(x)
                if ',' in s or '"' in s or '\n' in s:
                    s = '"' + s.replace('"', '""') + '"'
                return s
            lines.append(",".join(esc(rd.get(f,"")) for f in fields))
        csv_text = "\n".join(lines)
        csv_bytes = ("\ufeff" + csv_text).encode("utf-8")   # 前置 UTF-8 BOM

        media = anvil.BlobMedia("text/plain", csv_bytes, "export.csv")
        anvil.media.download(media)

    # ---------------- 内部过滤 ----------------
    def _apply_filter(self):
        def ok(row):
            rd = dict(row)
            for f, vals in self.filter_set.items():
                if not vals:
                    continue
                cell = str(rd.get(f, ""))
                if not any(v in cell for v in vals):
                    return False
            return True
        return [r for r in self.all_rows if ok(r)]

    # ---------------- 向外抛结果 ----------------
    def _emit_rows(self, rows):
        if self.on_search:
            self.on_search(rows)
        else:
            self.raise_event('x-search', rows=rows)
