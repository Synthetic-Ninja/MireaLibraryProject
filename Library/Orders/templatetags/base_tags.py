from django import template

register = template.Library()


@register.filter(name='get_status_color')
def get_status_color(status: str) -> str:
    match status:
        case 'created':
            return 'table-light'

        case 'processing':
            return 'table-secondary'

        case 'canceled':
            return 'table-danger'

        case 'overdue':
            return 'table-warning'

        case 'issued':
            return 'table-info'

        case 'complete':
            return 'table-success'

        case _:
            return 'table-light'
