/**
 * Created by Admin on 2015/10/04.
 */
var id = 0;
var deleteid = 0;
var shareid = 0;
var count = 0;
$(function () {
    $('tr.context').contextMenu('myMenu1',
        {
            bindings: {
                'edit': function (t) {
                    id = t.id;
                    $(".update").attr('value', id);
                    $('[data-remodal-id=modalup]').remodal();
                },
                'delete': function (t) {
                    deleteid = t.id;
                    $(".delete").attr('value', deleteid);
                    $('[data-remodal-id=deleteModal]').remodal()
                },
                'share': function (t) {
                    shareid = t.id;
                    $(".share").attr('value', shareid);
                    if (count == 0) {
                        $.ajax({
                            url: "check_friend",
                            dataType: 'html',
                            type: 'POST'
                        }).done(function (data) {
                            $('.shareContainer').html($(data).find(".friendContainer").children());
                        });
                        count += 1;
                    }
                    $('[data-remodal-id=shareModal]').remodal()
                },
                'test': function (t) {
                    $('[data-remodal-id=modal]').remodal();
                }
            }
        });
    $(li).click(function () {
        $(this).css()
    })
});