$(document).ready(function () {

    var d = $('#data').text();
    let darray = d.replace('[', '').replace(']', '').split(",").map(Number);
    var l = $('#labels').text();
    let larray = l.replace('[', '').replace(']', '').replaceAll("'", '').split(",").map(String);
    var qu_text = $('#qu').text();
    let qu_text_array = qu_text.replace('[', '').replace(']', '').replaceAll("'", '').split(",").map(String);
    var qu_id = $('#qu_id').text();
    let qu_id_array = qu_id.replace('[', '').replace(']', '').replaceAll("'", '').split(",").map(Number);
    var op_num = $('#op_num').text();
    let op_num_array = op_num.replace('[', '').replace(']', '').replaceAll("'", '').split(",").map(Number);

    console.log('darray: ', darray)
    console.log('larray:', larray)
    console.log("qu_text_array:", qu_text_array)
    console.log("qu_id_array:", qu_id_array)
    console.log("op_num_array:", op_num_array)



    var back = ['#5bc0de', '#cbecf7', '#79d4f0', '#ace0f0', '#ace0f5']
    var config = []
    for (let i = 0; i < qu_id_array.length; i++) {
        var data = []
        var labels = []
        var qu = qu_text_array[i]
        if (i > 0)
            pre_op_num = op_num_array[i - 1] - 1

        else
            pre_op_num = 0

        for (let j = i * pre_op_num; j < op_num_array[i] + (pre_op_num) + i; j++) {
            data.push(darray[j])
            labels.push(larray[j])
        }
        console.log("data", data)
        console.log("labels", labels)

        config[i] = {
            type: 'pie',
            data: {
                datasets: [{
                    data: data,
                    backgroundColor: back,
                    label: qu
                }],
                labels: labels,
            },
            options: {
                responsive: true
            }
        };
    }

    $('#view').click(function () {
        var ctx
        for (let i = 0; i < qu_id_array.length; i++) {
            var chart_id = 'qu' + qu_id_array[i].toString()
            console.log(chart_id)
            ctx = document.getElementById(chart_id).getContext('2d');
            window.myPie = new Chart(ctx, config[i]);
        }
    });
});