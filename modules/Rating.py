def get_Rating(metadata):
    # 从元数据中获取 audienceRating
    audience_rating = metadata.get('audienceRating')
    if audience_rating is not None:
        # 将 audience_rating 转换为字符串
        audience_rating = str(audience_rating)
    return audience_rating
