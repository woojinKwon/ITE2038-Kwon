$(document).ready(() => {
    // var container = document.getElementById('map'); //지도를 담을 영역의 DOM 레퍼런스
    var item= [];
    var markers = [];
    var container = $("#map").get(0) //map 이라는 id를 가진 것들을 배열로 받는데, 그중 인덱스0을 get하겠다
    var options = { //지도를 생성할 때 필요한 기본 옵션
      center: new kakao.maps.LatLng(37.55837671, 127.050856), //지도의 중심좌표.
      level: 3 //지도의 레벨(확대, 축소 정도)
    };
    var map = new kakao.maps.Map(container, options);
    var find_result
    var infowindow = new kakao.maps.InfoWindow({zIndex:1})
    var click_infowindow = new kakao.maps.InfoWindow({
      removable : true
    })
    var bounds = new kakao.maps.LatLngBounds()
    var d = new Date();
    /*
    $.ajax({
      url: "/",
      cache: false}).done(data =>{
          console.log(data)
    $("#search").submit((e) => {
      e.preventDefault()
      var places = new kakao.maps.services.Places();
  
      var callback = function(result, status) {
        if (status === kakao.maps.services.Status.OK) {
          console.log(result)
          find_result = result
         
           let tBodyHtml = ''
    for(let row of find_result){
      
        tBodyHtml += `<tr>
            <td>${row["place_name"]}</td>
            <td>${row["address_name"]}</td>
            <td><form method = "POST" id = "find_one" action= "/position">
  <button type="submit" name="find" value1=${row["x"]} value2 = ${row["y"]} >장소검색</button>
  </form></td>
            </tr>`
    }
    $('table tbody').html(tBodyHtml)
        }
    }
    
    places.keywordSearch(e.target.place.value, callback)
  
    })
  
  })*/

  
  /************************약국 이름 검색****************************/
    $("#search").submit((e)=>{
      e.preventDefault()
        dictData = {
          "data_name": e.target.name.value,
          "table_name" : "store"
        }
        $.ajax({
          type:"POST",
          url: "/name_search",
          cache: true,
          data: JSON.stringify(dictData),
          contentType: "application/json",
          success: res=>{
            if(res["result"]=="fail"){
              alert("검색결과가 없습니다")
              return
            }
            else{
            item = JSON.parse(res)
            display(item)
            }
          }
        })
    })
  
  //**************************주변 검색***************************
    $("#here").click(() => {
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition((position) => {  //callback임 
  
          let formData={
            "lat" : position.coords.latitude,
            "lng" : position.coords.longitude
          }
      
          $.ajax({
            type: "POST",
            url: "/store_api",
            cache: true,
            async: true,
            data: JSON.stringify(formData),
            contentType: "application/json",
            success: res=>{
                item = JSON.parse(res)
                display(item)
            }
            
          })
          //위치를 알수있는 scope 이 이후에는 사라짐
        })
  
        } else {
        x.innerHTML = "Geolocation is not supported by this browser.";
      }
    })
  
  
  
    function addMarker(position, idx) {
       
        var marker = new kakao.maps.Marker({
                position: position,// 마커의 위치
                clickable: true
            });
        marker.setMap(map); 
        markers.push(marker); 
       
        return marker
    }
  
    function removeMarker() {
      for ( var i = 0; i < markers.length; i++ ) {
          markers[i].setMap(null);
      }   
      markers = [];
    }
  
    function getListItem(index, places) {
  
      var el = document.createElement('li'),
      itemStr = '<div class="info">' +
                  '   <h5>' + places["name"] + '</h5>';
  
        itemStr += '    <p>' +  places["address"]  + '</p>'; 
        if(places["start_time"]<= d.getHours() && places["end_time"] > d.getHours()){
          itemStr += '<h3 class="opened">';
        }
        else{
          itemStr += '<h3 class="closed">';
        }
        itemStr += '영업시간 : 오전 '+places["start_time"]+'시 ~ 오후 '
                                     +(places["end_time"] -12) + '시</h3>';
        

          itemStr += ' <form method ="POST" action= "/reservation_store">'+
                      '<button type= "submit" id = "submit" name = "submit" value = "'+ places["id"] + 
                      '">예약하기</button>'+
                      '</form>';
        
      el.innerHTML = itemStr;
      el.className = 'item';
  
      return el;
  }
  
  function displayInfowindow(marker, title) {
    var content = '<div style="padding:5px;z-index:1;">' + title + '</div>';
  
    infowindow.setContent(content);
    infowindow.open(map, marker);
  }
  function display(item){
    removeMarker()
    var listEl = document.getElementById('placesList')
    var menuEl = document.getElementById('menu_wrap')
    var fragment = document.createDocumentFragment()        
    var i = 0
    removeAllChildNods(listEl)
    for(row of item){
    var coords = new kakao.maps.LatLng(row["lat"], row["lng"])
    itemEl = getListItem(i, row)
    marker= addMarker(coords,i)
    bounds.extend(coords);
    click_iwContent = getListItem(i,row);
    (function(marker, title,info) {
      kakao.maps.event.addListener(marker, 'mouseover', function() {
          displayInfowindow(marker, title);
      });
  
      kakao.maps.event.addListener(marker, 'mouseout', function() {
          infowindow.close();
      });
      kakao.maps.event.addListener(marker, 'click', function() {
        click_infowindow.setContent(info)
        click_infowindow.open(map,marker);
      })
  
      itemEl.onmouseover =  function () {
          displayInfowindow(marker, title);
      };
  
      itemEl.onmouseout =  function () {
          infowindow.close();
      };
    })(marker, row['name'],click_iwContent);
    fragment.appendChild(itemEl);
    i= i+1
  }
     // 검색결과 항목들을 검색결과 목록 Elemnet에 추가합니다
  listEl.appendChild(fragment);
  menuEl.scrollTop = 0;
  map.setBounds(bounds);
  }
  
  function display_subject(item){
    removeMarker()
    var listEl = document.getElementById('placesList')
    var menuEl = document.getElementById('menu_wrap')
    var fragment = document.createDocumentFragment()        
    var i = 0
    removeAllChildNods(listEl)
    for(row of item){
    var coords = new kakao.maps.LatLng(row[0]["lat"], row[0]["lng"])
    itemEl = getListItem(i, row[0])
    marker= addMarker(coords,i)
    bounds.extend(coords);
    click_iwContent = getListItem(i,row[0]);
    (function(marker, title,info) {
      kakao.maps.event.addListener(marker, 'mouseover', function() {
          displayInfowindow(marker, title);
      });
  
      kakao.maps.event.addListener(marker, 'mouseout', function() {
          infowindow.close();
      });
      kakao.maps.event.addListener(marker, 'click', function() {
        click_infowindow.setContent(info)
        click_infowindow.open(map,marker);
      })
  
      itemEl.onmouseover =  function () {
          displayInfowindow(marker, title);
      };
  
      itemEl.onmouseout =  function () {
          infowindow.close();
      };
    })(marker, row[0]['name'],click_iwContent);
    fragment.appendChild(itemEl);
    i= i+1
  }
     // 검색결과 항목들을 검색결과 목록 Elemnet에 추가합니다
  listEl.appendChild(fragment);
  menuEl.scrollTop = 0;
  map.setBounds(bounds);
  }
  
  function removeAllChildNods(el) {   
    while (el.hasChildNodes()) {
        el.removeChild (el.lastChild);
    }
  }
  })