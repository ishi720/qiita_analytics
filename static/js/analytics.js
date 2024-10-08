var chartContainer;
var myLineChart;

document.addEventListener('DOMContentLoaded', function() {

    chartContainer = document.getElementById("chartContainer");


    get_like_date();

});

function get_like_date() {
    const urlParams = new URLSearchParams(window.location.search);
    const item_id = urlParams.get('item_id');
    const url = './api/get_item_like?item_id='+ item_id;

    // リクエストを送信
    fetch(url)
    .then(response => response.json())
    .then(data => {
        document.getElementById("item_title").innerHTML = data.title;
        document.getElementById("item_url").href = data.url;
        document.getElementById("item_user_id").innerHTML = data.user_id;
        document.getElementById('item_user_profile_image_url').src = data.user_profile_image_url;
        let keys = Object.keys(data.likes);
        let values = Object.values(data.likes);
        render_chart(keys, values);
    })
    .catch(error => {
        // エラーハンドリング
        console.error('Error fetching data:', error);
    });
}

function createDateList(start, end) {
    var startDate = new Date(start);
    var endDate = new Date(end);
    var dateList = [];

    // 開始日から終了日までの日付を生成し、リストに追加
    var currentDate = new Date(startDate);
    while (currentDate <= endDate) {
        var formattedDate = currentDate.toISOString().slice(0, 10);
        dateList.push(formattedDate);
        currentDate.setDate(currentDate.getDate() + 1);
    }

    return dateList;
}


function render_chart(keys, values){


    let theDayBefore = moment(keys[0]).clone().subtract(1, "days").format('YYYY-MM-DD');
    keys.unshift(theDayBefore);
    values.unshift(0);

    // データ
    const data = {
        // labels: keys.map((value) => moment(value).toDate()),
        labels: keys,
        datasets: [{
            label: 'いいね数',
            tension: 0.2,
            data: values,
            borderColor: "green",
            backgroundColor: "rgba(0,255,0,0.2)",
            fill: true
        }]
    };

    // データが欠落している日付に対応するデータを0に設定
    var newData = [];
    var allDates = createDateList(keys[0], keys[keys.length - 1]) // 期間内の全日付
    var existingDates = data.labels;
    for (var i = 0; i < allDates.length; i++) {
        if (existingDates.includes(allDates[i])) {
            newData.push(data.datasets[0].data[existingDates.indexOf(allDates[i])]);
        } else {
            newData.push(0);
        }
    }
    data.labels = allDates

    newData = transformArray(newData);//右肩上がりの加算したデータに変換

    data.datasets[0].data = newData;

    // グラフのオプション
    const options = {
        responsive: true,
        scales: {
            x: {
                type: 'time',
                time: {
                    unit: 'day',
                    displayFormats: {
                        'day': 'YYYY-MM-DD'
                    }
                }
            },
            y: {
                min: 0
            }
        }
    };

    // ローディングを非表示
    const loadingDiv = document.querySelector("div.loading");
    if (loadingDiv) {
        loadingDiv.style.display = "none";
    }

    // グラフを描画
    const ctx = document.getElementById('myLineChart');
    myLineChart = new Chart(ctx, {
        type: 'line',
        data: data,
        options: options
    });
    resizeChart();

    // ウィンドウのリサイズ時にチャートのサイズを調整する
    window.addEventListener('resize', resizeChart);
}


function transformArray(arr) {
    if (arr.length === 0) {
        return []; // 空配列の場合は空配列を返す
    }

    let transformedArray = [arr[0]]; // 最初の要素はそのまま残す

    for (let i = 1; i < arr.length; i++) {
        transformedArray.push(transformedArray[i - 1] + arr[i]); // 各要素を変換して新しい配列に追加する
    }

    return transformedArray;
}

function resizeChart() {
    myLineChart.resize(chartContainer.clientWidth, "auto");
}