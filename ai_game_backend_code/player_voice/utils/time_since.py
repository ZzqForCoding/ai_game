from django.utils import timezone
import math

def time_since_zh(value):
    now = timezone.now()
    diff = now - value

    if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
        return '刚刚'
    if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 60 * 60:
        return str(math.floor(diff.seconds / 60)) + "分钟前"
    if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 24 * 60 * 60:
        return str(math.floor(diff.seconds / 3600)) + "小时前"
    if diff.days >= 1 and diff.days < 30:
        return str(diff.days) + "天前"
    if diff.days >= 30 and diff.days < 365:
        return str(math.floor(diff.days / 30)) + "个月前"
    if diff.days >= 365:
        return value.strftime("%Y-%m-%d %H:%M:%S")
