from django import template
from django.utils.safestring import mark_safe

register = template.Library()

TEMP1 = """
<div class='content' style='margin-left:%s;'>
    <span>%s</span>
"""


def generate_comment_html(sub_comment_dic, margin_left_val):
    html = '<div class="comment">'
    for k, v_dic in sub_comment_dic.items():
        # 因为是子评论了，所以需要加上margin_left_val（30）像素的偏移量，子子评论再加margin_left_val（30）的偏移量，以此类推。
        html += TEMP1 % (margin_left_val, k[1])

        # 只要有字典，就递归的往下执行generate_comment_html()函数
        if v_dic:
            html += generate_comment_html(v_dic, margin_left_val)
        html += "</div>"
    html += "</div>"
    return html


@register.simple_tag
def tree(comment_dic):
    # 将comment_dic字典里的数据拼接成html传给前端
    html = '<div class="comment">'
    for k, v in comment_dic.items():
        # 因为是根评论，所以margin-left应该是0，所以这里传入（0，k[1]），k[1]是评论内容
        html += TEMP1 % (0, k[1])
        # 如果v不为空字典，则执行generate_comment_html()
        if v:
            html += generate_comment_html(v, 30)
        html += "</div>"
    html += '</div>'

    return mark_safe(html)