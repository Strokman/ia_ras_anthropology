var newSelect = document.getElementById('federal_district');
newSelect.setAttribute('onchange', 'run(this.value)');

    function run(value) {
        var federal_d_num = value;
        var region_select = document.getElementById("region");

        fetch('/submit/get_region/' + federal_d_num).then(function(response) {
        response.json().then(function(data) {
        var optionHTML = '';

                    for (var region of data.regions) {
                        optionHTML += '<option value="' + region.id + '">' + region.name + '</option>';
                    }

                    region_select.innerHTML = optionHTML;
        });
        });
    }