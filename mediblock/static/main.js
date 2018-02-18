$(document).ready(function () {
    $('.materialboxed').materialbox();

    var options = [
        {
            selector: '.main', offset: 300, callback: function (el) {
                Materialize.fadeInImage($(el));
            }
        },
        {
            selector: '.blockchain', offset: 150, callback: function (el) {
                Materialize.showStaggeredList($(el));
            }
        },
        {
            selector: '#chart', offset: 500, callback: function (el) {
                Materialize.fadeInImage($(el));
            }
        },
    ];
    Materialize.scrollFire(options);


    // $(".profile").sideNav();
    $(".profile").sideNav({
        menuWidth: 1000,
        edge: 'right',
        closeOnClick: true,
        draggable: true,
        onOpen: function (el) /**/{
        },
        onClose: function (el) {
        },
    });

});