import re
import dateparser


def parse_nl(text: str):
    txt = text.lower()

    # count all videos
    if re.search(r"\bсколько всего видео\b|\bвсего видео\b", txt):
        return {"intent": "count_all_videos", "params": {}}

    # count by creator and period
    m = re.search(r"креатор.*id[:\s]*([0-9a-z\-]+).*с\s*(.+?)\s*по\s*(.+)", txt)
    if m:
        creator = m.group(1)
        d1 = dateparser.parse(m.group(2), languages=["ru"])
        d2 = dateparser.parse(m.group(3), languages=["ru"])
        if d1 and d2:
            return {"intent": "count_videos_by_creator_period",
                    "params": {"creator_id": creator, "date_from": d1.date().isoformat(),
                               "date_to": d2.date().isoformat()}}

    # threshold views
    m = re.search(r"больше\s*([\d\s]+)\s*просм", txt)
    if m:
        n = int(m.group(1).replace(" ", ""))
        return {"intent": "count_videos_over_views", "params": {"views_threshold": n}}

    # sum delta views by date
    m = re.search(r"сумм[а|е].*просмотров.*(\d{1,2}\s*\w+\s*\d{4})", txt)
    if m:
        d = dateparser.parse(m.group(1), languages=["ru"])
        if d:
            return {"intent": "sum_delta_views_by_date", "params": {"date": d.date().isoformat()}}

    # new views on date
    m = re.search(r"нов(ы|ых).*просмотр", txt) or re.search(r"получали новые просмотры\s*(\d{1,2}\s*\w+\s*\d{4})", txt)
    m2 = re.search(r"(\d{1,2}\s*\w+\s*\d{4})", txt)
    if m2 and ("нов" in txt or "получали" in txt):
        d = dateparser.parse(m2.group(1), languages=["ru"])
        if d:
            return {"intent": "count_videos_with_new_views_on_date", "params": {"date": d.date().isoformat()}}

    return {"intent": "unknown", "params": {}}
