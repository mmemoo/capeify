from lxml import etree
import os

templates_dir = os.path.abspath(__file__)
templates_dir = os.path.dirname(os.path.dirname(templates_dir))


def create_cursor(
    cursor, framecount, frameduration, hotspotx, hotspoty, pointshigh, pointswide, data
):
    template = etree.parse(templates_dir + "/templates/cursor_template.cape")
    template = template.getroot()

    key_ = template[0]
    key_.text = str(cursor)

    dict_ = template[1]

    framecount_ = dict_[1]
    framecount_.text = str(framecount)

    frameduration_ = dict_[3]
    frameduration_.text = str(frameduration)

    hotspotx_ = dict_[5]
    hotspotx_.text = str(hotspotx)

    hotspoty_ = dict_[7]
    hotspoty_.text = str(hotspoty)

    pointshigh_ = dict_[9]
    pointshigh_.text = str(pointshigh)

    pointswide_ = dict_[11]
    pointswide_.text = str(pointswide)

    array = dict_[13]
    data_ = array[0]
    data_.text = str(data)

    return template


def create_cape(author, capename, cursors, identifier):
    template = etree.parse(templates_dir + "/templates/cape_template.cape")

    dict_ = template.getroot()

    author_ = dict_[1]
    author_.text = str(author)

    capename_ = dict_[3]
    capename_.text = str(capename)

    identifier_ = dict_[13]
    identifier_.text = str(identifier)

    cursors_ = dict_[9]
    for cursor in cursors:
        cursors_.append(cursor[0])
        cursors_.append(cursor[0])

    template = dict_.getroottree()

    return template
