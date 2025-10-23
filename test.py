
    # 更新视图
    def update_table(self, filtered_rows):
        self.parent_item.repeat.items = filtered_rows  

        # 样式控制 文字单元格太长都省略掉
        for row_tpl in self.parent_item.repeat.get_components():
            row_comps = row_tpl.get_components()
            cols = self.parent_item.grid.columns  
            for comp in row_comps:
                col_index = row_comps.index(comp)
                col_info = cols[col_index] 
                if not isinstance(comp, anvil.Label):
                    continue

                node = anvil.js.get_dom_node(comp).querySelector("span")

                # 文本处理
                node.style.whiteSpace = "nowrap"
                node.style.overflow = "hidden"
                node.style.textOverflow = "ellipsis"
                node.style.maxWidth = "70px"


                # 超链接处理
                text = node.innerHTML or ""
                if 'url' in (col_info.get('data_key') or ''):
                    node.innerHTML = f'<a href="{text}" target="_blank" >{text}</a>'

                # 图片处理
                if 'img' in (col_info.get('data_key') or ''):
                    b64 = (comp.text or "").strip()
                    src = f"data:image/png;base64,{b64}"


                    # 1) 生成一个 btn 组件替换掉原来的 Label
                    btn = anvil.Button(text="查看图", tooltip="点击查看原图")
                    btn.set_event_handler('click',lambda **x:alert(anvil.Image(source=src )))  

                    # 3) 用同一列位置替换组件
                    row_tpl.add_component(btn, column=col_info['id'])
                    comp.remove_from_parent()  

