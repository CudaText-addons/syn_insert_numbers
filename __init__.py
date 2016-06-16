from sw import *

class Command:
    def run(self):
        carets = ed.get_carets()
        if carets and len(carets)!=1:
            msg_status('Cannot handle multi-carets')
            return

        x0, y0 = ed.get_caret_xy()
        line1, line2 = ed.get_sel_lines()
        offset, nlen = ed.get_sel()
        use_sel = nlen>0

        text_info = 'Specified count of lines will be inserted' if not use_sel else 'Selected lines will be changed'
        
        id_prefix = 1
        id_startnum = 3
        id_digits = 5
        id_suffix = 7
        id_onlytext = 8
        id_skipempty = 9
        id_afterlead = 10
        id_repeat = 12
        id_ok = 14
        
        c1 = chr(1)
        res = dlg_custom('Insert Numbers', 600, 220, '\n'.join([]
          +[c1.join(['type=label', 'cap=&Prefix:', 'pos=6,6,200,0'])]
          +[c1.join(['type=edit', 'val=', 'pos=6,24,194,0'])]
          +[c1.join(['type=label', 'cap=Start &num:', 'pos=200,6,300,0'])]
          +[c1.join(['type=spinedit', 'val=1', 'props=-1000,1000000,1', 'pos=200,24,294,0'])]
          +[c1.join(['type=label', 'cap=&Digits:', 'pos=300,6,400,0'])]
          +[c1.join(['type=spinedit', 'val=1', 'props=1,20,1', 'pos=300,24,394,0'])]
          +[c1.join(['type=label', 'cap=&Suffix:', 'pos=400,6,600,0'])]
          +[c1.join(['type=edit', 'val=', 'pos=400,24,594,0'])]
          +[c1.join(['type=check', 'cap=&Use only prefix+suffix', 'pos=6,54,500,0'])]
          +[c1.join(['type=check', 'cap=Skip &empty lines', 'pos=6,80,500,0', 'val=1', 'en='+str(int(use_sel)) ])]
          +[c1.join(['type=check', 'cap=Insert &after leading spaces', 'pos=6,106,500,0', 'en='+str(int(use_sel)) ])]
          +[c1.join(['type=label', 'cap=&Repeat counter:', 'en='+str(int(not use_sel)), 'pos=6,130,100,0'])]
          +[c1.join(['type=spinedit', 'val=4', 'props=1,2000000,1', 'en='+str(int(not use_sel)), 'pos=6,150,100,0'])]
          +[c1.join(['type=label', 'cap='+text_info, 'pos=6,190,400,0'])]
          +[c1.join(['type=button', 'cap=&OK', 'props=1', 'pos=400,190,494,0'])]
          +[c1.join(['type=button', 'cap=Cancel', 'pos=500,190,594,0'])]
          ))
        if res is None: return
        
        (btn, text) = res
        if btn!=id_ok: return
        text = text.splitlines()

        s_prefix = text[id_prefix]
        n_startnum = int(text[id_startnum])
        n_digits = int(text[id_digits])
        s_suffix = text[id_suffix]
        n_repeat = int(text[id_repeat])
        b_onlytext = bool(int(text[id_onlytext])) 
        b_skipempty = bool(int(text[id_skipempty])) 
        b_afterlead = bool(int(text[id_afterlead])) 
        
        text_repeat = 'repeat %d'%n_repeat if not use_sel else 'selection'
        text_onlytext = 'only text' if b_onlytext else ''
        print('Insert numbers: prefix "%s", start %d, digits %d, suffix "%s", %s, %s' % \
              (s_prefix, n_startnum, n_digits, s_suffix, text_repeat, text_onlytext))
        s_format_str = '%0'+str(n_digits)+'d'
                                                            
        if use_sel:
            number = n_startnum
            for i in range(line1, line2+1):
                s_prev = ed.get_text_line(i)
                s_indent = ''
                
                if b_skipempty:
                    if not s_prev.strip():
                        continue
                        
                if b_afterlead:
                    n = 0
                    while n<len(s_prev) and s_prev[n] in (' ', '\t'): n += 1
                    s_indent = s_prev[:n]
                    s_prev = s_prev[n:]
                        
                if b_onlytext:
                    s = s_indent + s_prefix + s_prev + s_suffix
                else:
                    s = s_indent + s_prefix + s_format_str%(number) + s_suffix + s_prev
                    number += 1
                ed.set_text_line(i, s)
        else:
            items = []
            for i in range(n_repeat):
                s = '' if b_onlytext else s_format_str%(n_startnum+i)
                items += [s_prefix + s + s_suffix]
            items += ['']    
            
            eol = ed.get_prop(PROP_EOL)
            ed.set_caret_xy(0, y0)
            ed.insert(eol.join(items))
            
        msg_status('Numbers inserted')
        