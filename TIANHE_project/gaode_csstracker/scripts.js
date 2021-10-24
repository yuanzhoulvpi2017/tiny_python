// grab all elements needed
let latitudeText = document.querySelector('.latitude');
let longitudeText = document.querySelector('.longitude');
let timeText = document.querySelector('.time');
let speedText = document.querySelector('.speed');
let altitudeText = document.querySelector('.altitude');
let visibilityText = document.querySelector('.visibility');

/* default latitude and longitude. Here lat and long is for "London" */
let lat = 51.505;
let long = -0.09;
let zoomLevel = 6;


var map = new AMap.Map('container', {
    resizeEnable: true, //是否监控地图容器尺寸变化
    zoom: zoomLevel, //初始化地图层级
    center: [long, lat] //初始化地图中心点
});

var icon = new AMap.Icon({
    size: new AMap.Size(90, 90),    // 图标尺寸
    image: 'css500.jpg',  // Icon的图像
    // imageOffset: new AMap.Pixel(0, -60),  // 图像相对展示区域的偏移量，适于雪碧图等
    imageSize: new AMap.Size(90, 90)   // 根据所设置的大小拉伸或压缩图片
});

var marker = new AMap.Marker({
    position: new AMap.LngLat(long, lat),
    offset: new AMap.Pixel(-10, -10),
    icon: icon, // 添加 Icon 实例
    title: '空间站',
    zoom: zoomLevel
});

map.add(marker);


// findCSS() function definition
function findCSS() {
    fetch("http://127.0.0.1:8000/csslocation")
        .then(response => response.json())
        .then(data => {
            data = data[0]
            lat = data.latitude.toFixed(2);
            long = data.longitude.toFixed(2);
            // convert seconds to milliseconds, then to UTC format
            // const timestamp = new Date(data.time * 1000).toUTCString();
            const timestamp = data['time_format']
            // const speed = data.velocity.toFixed(2);
            const altitude = data.altitude.toFixed(2);
            // const visibility = data.visibility;
            // call updateCSS() function to update things
            updateCSS(lat, long, timestamp, altitude);
        })
        .catch(e => console.log(e));
}

// updateCSS() function definition
function updateCSS(lat, long, timestamp, altitude) {
    // updates map view according to Marker's new position
    map.setCenter([long, lat])

    // updates Marker's lat and long on map

    marker.setPosition([long, lat])

    // updates other element's value
    latitudeText.innerText = lat;
    longitudeText.innerText = long;
    timeText.innerText = timestamp;
    // speedText.innerText = `${speed} km/hr`;
    altitudeText.innerText = `${altitude} km`;
    // visibilityText.innerText = visibility;


}

findCSS()
/* call findCSS() initially to immediately set the CSS location */
// findCSS();

// call findCSS() for every 2 seconds
setInterval(findCSS, 2000);