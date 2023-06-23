    var map = L.map('map').setView([47.24404064687492, 41.950575933368334], 7);
    L.tileLayer('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png', {
    maxZoom: 17,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'}).addTo(map);
    setInterval(function () {
        map.invalidateSize();
        }, 100);
    {% for i in sites %}
    {% if i.sr %}
    var marker = L.marker([{{i.lat}}, {{ i.long}}]).addTo(map).bindPopup('{{i.name}}, SR: {{i.sr}}, sample type: {{i.sample_type}}');
    {% endif %}
    {% if not i.sr %}
    var marker = L.marker([{{i.lat}}, {{ i.long}}]).addTo(map).bindPopup('{{i.name}}');
    {% endif %}
    {% endfor %}