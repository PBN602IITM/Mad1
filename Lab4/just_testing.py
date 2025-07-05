
import pyhtml as html

table = {'table': [[1,2,3],[4,5,6]]}

def f_table(ctxt):
    template_str = html.html(
        html.head(
            html.title('Title')
        ),
        html.body(
            html.table(
                (html.tr(
                    html.td(cell) for cell in row
                ) for row in ctxt['table'])
            )
        )
    )
    return (template_str)

template = f_table(table)
print(template.render())