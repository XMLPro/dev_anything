/**
 * Created by Admin on 2015/10/11.
 */
$(
    $(window).load(function () {
        array = [];
        $.ajax({
            type: 'POST',
            url: '/jsonGet',
            dataType: 'json'
        }).done(function (data) {
            $.each(data, function (key, value) {
                array.push(value);
            })

            var lineChartData = {
                //x軸の情報
                labels: ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月'],
                //各グラフの情報。複数渡すことができる。
                datasets: [
                    {
                        fillColor: "rgba(220, 220, 220, 0.5)",
                        strokeColor: "rgba(220, 220, 220, 1)",
                        pointColor: "rgba(220, 220, 220, 1)",
                        pointStrokeColor: "#fff",
                        //実際のデータ
                        data: array
                    }
                ]
            }

            var option = {
                //縦軸の目盛りの上書き許可。これ設定しないとscale関連の設定が有効にならないので注意。
                scaleOverride: true,

                //以下設定で、縦軸のレンジは、最小値0から5区切りで35(0+5*7)までになる。
                //縦軸の区切りの数
                scaleSteps: 10000,
                //縦軸の目盛り区切りの間隔
                scaleStepWidth: 1000,
                //縦軸の目盛りの最小値
                scaleStartValue: 0,

                //アニメーション設定
                animation: false,

                //Y軸の表記（単位など）
                scaleLabel: "<%=value%>円",

                //ツールチップ表示設定
                showTooltips: false,

                //ドットの表示設定
                pointDot: false,

                //線を曲線にするかどうか。falseで折れ線になる。
                bezierCurve: false
            }

            var ctx = $('#lineChartCanvas')[0].getContext("2d");
            new Chart(ctx).Line(lineChartData, option);

        })
    })
)
;