function highlightActiveTab() {
    // Получаем адрес текущей страницы
    var url = window.location.pathname;
    // проверяем главная это страница или нет
    if (url != '/') {
        urlRegExp = new RegExp(url.replace(/\/$/, ''));
        $('.tabbar a').each(function () {
            if (urlRegExp.test(this.href)) {
                $(this).parent().addClass('active');
            }
        });
    }
}

$(document).ready(highlightActiveTab);
