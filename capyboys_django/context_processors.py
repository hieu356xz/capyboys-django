def base_context(request):
    menu_links = [
        {
            "name": "Trang chủ",
            "link": "/",
        },
        {
            "name": "Sản phẩm",
            "link": "/collections/all",
        },
        {
            "name": "Bài viết",
            "link": "/blogs/tin-tuc",
        },
        {
            "name": "Giới thiệu",
            "link": "/about",
        },
    ]
    return {'menu_links': menu_links}