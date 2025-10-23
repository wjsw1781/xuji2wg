from ._anvil_designer import FilterBarTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil import *
import anvil.media
from anvil import *
from anvil import *
import anvil.media, re

DISPLAY_LIMIT = 10          # 弹窗最多展示的选项数

from ..utils import *

class FilterBar(FlowPanel):
    """
  rows       : list(dict/DataRow)  全量数据
  on_search  : 回调函数(filtered_rows)。未提供则抛 'x-search' 事件
  """

    def __init__(self, parent, on_search=None,on_new=None, **properties):
        super().__init__(**properties)
        
        # 添加一些关键属性以及缓存
        list_add_self_items(parent)
        
        rows = parent.repeat.items
        
        self.all_rows   = rows or []
        self.on_search  = on_search
        self.on_new  = on_new
        
        self.filter_set = {}            # {field:set(values)}
        self.inputs     = {}
        self.dist_cache = {}            # {field: (preview_list, total_cnt)}
        self.role       = 'filter-bar'
        self.spacing    = 'none'

        if not self.all_rows:
            return

        self.fields = list(dict(self.all_rows[0]).keys())

        # 生成输入框
        for f in self.fields:
            tb = TextBox(placeholder=f, width=140)
            tb.tag.field = f
            tb.set_event_handler('focus', self._open_selector)
            self.add_component(tb)
            self.inputs[f]     = tb
            self.filter_set[f] = set()

        # 搜索 + 导出按钮
        btn_new    = Button(text="新增",   icon="fa:plus",   role="raised")

        btn_search = Button(text="搜索", icon="fa:search", role="primary")
        btn_csv    = Button(text="导出CSV", icon="fa:download")
        btn_new.set_event_handler   ("click", self._do_new)

        btn_search.set_event_handler("click", self._do_search)
        btn_csv.set_event_handler("click", self._do_export)

        self.add_component(btn_new)

        self.add_component(btn_csv)

        self.add_component(btn_search)

    # --------------------------------------------------
    # 懒加载 distinct，截断到 DISPLAY_LIMIT
    # --------------------------------------------------
    def _get_preview_values(self, field):
        if field in self.dist_cache:
            return self.dist_cache[field]

        seen, preview = set(), []
        for r in self.all_rows:
            v = dict(r).get(field)
            if v is None:
                continue
            s = str(v)
            if s not in seen:
                seen.add(s)
                if len(preview) < DISPLAY_LIMIT:
                    preview.append(s)
        preview.sort()
        self.dist_cache[field] = (preview, len(seen))
        return self.dist_cache[field]

    # --------------------------------------------------
    # 弹窗：显示记忆 + 复选 + 手输
    # --------------------------------------------------
    def _open_selector(self, **e):
        tb     = e['sender']
        field  = tb.tag.field
        preview_vals, total_cnt = self._get_preview_values(field)
        already = set(self.filter_set[field])

        # 手动输入框（TextArea）
        manual = TextArea(placeholder="可输入，逗号/空格/回车分隔", height=70, width='100%')

        # 若已选值不在 preview 中，则填到手输区
        extras = sorted(already - set(preview_vals))
        if extras:
            manual.text = " ".join(extras)

        # 复选框列表
        pnl_checks = ColumnPanel()
        for v in preview_vals:
            cb = CheckBox(text=v)
            cb.checked = v in already
            pnl_checks.add_component(cb)

        if total_cnt > DISPLAY_LIMIT:
            pnl_checks.add_component(
                Label(text=f"...共 {total_cnt} 条，仅展示前 {DISPLAY_LIMIT} 条，其余请手动输入",
                      italic=True)
            )

        # 全选 / 清空
        def mark(flag):
            for c in pnl_checks.get_components():
                if isinstance(c, CheckBox):
                    c.checked = flag
            if flag:
                # 全选时，把 preview 值补到手输框里
                tokens = set(re.split(r'[\s,]+', manual.text)) if manual.text else set()
                tokens.update(preview_vals)
                manual.text = " ".join(sorted(tokens))
            else:
                manual.text = ""

        btn_all  = Button(text="全选",  width="48%", role="primary")
        btn_none = Button(text="清空",  width="48%")
        btn_all.set_event_handler("click",  lambda **k: mark(True))
        btn_none.set_event_handler("click", lambda **k: mark(False))
        fp_btn = FlowPanel(spacing="small")
        fp_btn.add_component(btn_all)
        fp_btn.add_component(btn_none)

        dlg = ColumnPanel()
        dlg.add_component(manual)
        dlg.add_component(fp_btn)
        dlg.add_component(pnl_checks)

        ok = alert(dlg, title=f"选择 / 输入  {field}",
                   buttons=[("确定", True), ("取消", False)])
        if not ok:
            return

        # 收集结果
        sel = {c.text for c in pnl_checks.get_components()
               if isinstance(c, CheckBox) and c.checked}

        if manual.text:
            tokens = re.split(r"[\s,]+", manual.text)
            sel.update(t for t in tokens if t)

        self.filter_set[field] = sel
        tb.text = " ".join(sel)

    # --------------------------------------------------
    # 过滤
    # --------------------------------------------------
    def _apply_filter(self):
        def hit(row):
            rd = dict(row)
            for f, vals in self.filter_set.items():
                if not vals:
                    continue
                cell = str(rd.get(f, ""))
                if not any(v in cell for v in vals):
                    return False
            return True
        return [r for r in self.all_rows if hit(r)]

    # --------------------------------------------------
    # 搜索
    # --------------------------------------------------
    def _do_search(self, **e):
        self._emit_rows(self._apply_filter())

    # --------------------------------------------------
    # 导出 CSV（前端）
    # --------------------------------------------------
    def _do_export(self, **e):
        rows = self._apply_filter()
        if not rows:
            alert("无可导出的数据！")
            return

        fields = self.fields
        def esc(x):
            s = str(x)
            if any(c in s for c in (",", '"', "\n")):
                s = '"' + s.replace('"', '""') + '"'
            return s
        lines = [",".join(fields)]
        for r in rows:
            rd = dict(r)
            lines.append(",".join(esc(rd.get(f, "")) for f in fields))
        csv_txt = "\n".join(lines)
        blob = anvil.BlobMedia("text/plain", ("\ufeff" + csv_txt).encode("utf-8"),
                               "export.csv")
        anvil.media.download(blob)
    

    # --------------------------------------------------
    # 抛结果
    # --------------------------------------------------
    def _emit_rows(self, rows):
        if self.on_search:
            self.on_search(rows)
        else:
            self.raise_event("x-search", rows=rows)
            
    # 新增数据
    def _do_new(self, **e):
        pnl   = ColumnPanel()
        edits = {}
        
        for f in self.fields:
            fp = FlowPanel()
            fp.add_component(Label(text=f, width=100))
            tb = TextBox(width=200)
            fp.add_component(tb)
            pnl.add_component(fp)
            edits[f] = tb
        
        ok = alert(pnl, title="新建记录", buttons=[("确定", True), ("取消", False)])
        if not ok:
            return
        
        new_row = {f: edits[f].text for f in self.fields}
        
        # 交给外部处理（例如写入数据库、刷新表格等）
        if self.on_new:
            self.on_new(new_row)
        else:
            self.raise_event("x-new", row=new_row)
