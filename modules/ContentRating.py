def get_ContentRating(metadata):
    # 从元数据中获取内容分级信息
    contentRating = metadata.get('contentRating', None)

    # 如果内容分级为 "Not Rated"，将其转换为 "NR"
    if contentRating == 'Not Rated':
        contentRating = 'NR'

    return contentRating
