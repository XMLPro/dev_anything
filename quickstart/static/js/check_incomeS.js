/**
 * Created by Admin on 2015/10/04.
 */
$(function () {
    var id = 0;
    var deleteid = 0;
    var shareid = 0;
    var count = 0;
    $('tr.context').contextMenu('myMenu1',
        {
            bindings: {
                'edit': function (t) {
                    id = t.id;
                    $("#textarea0").attr('value', id);
                    $('[data-remodal-id=modalup]').remodal();
                },
                'delete': function (t) {
                    deleteid = t.id;
                    $(".delete").attr('value', deleteid);
                    $('[data-remodal-id=deleteModal]').remodal()
                }
            }
        });
});



