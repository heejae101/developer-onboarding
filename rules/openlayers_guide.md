# OpenLayers 개발 가이드

## 1. 개요
OpenLayers는 웹 브라우저에서 동적인 지도를 표시하기 위한 고성능 오픈소스 JavaScript 라이브러리입니다.
본 프로젝트에서는 `ol` 패키지를 사용하여 GIS 기능을 구현합니다.

## 2. 기본 맵 초기화 (Basic Map Initialization)
지도를 생성하기 위해서는 `Map`, `View`, `Layer`가 필요합니다.

```javascript
import Map from 'ol/Map';
import View from 'ol/View';
import TileLayer from 'ol/layer/Tile';
import OSM from 'ol/source/OSM';
import { fromLonLat } from 'ol/proj';

const map = new Map({
  target: 'map-container', // HTML 요소 ID
  layers: [
    new TileLayer({
      source: new OSM() // 오픈스트리트맵 소스
    })
  ],
  view: new View({
    center: fromLonLat([126.9780, 37.5665]), // 서울 시청 좌표 (경도, 위도)
    zoom: 12
  })
});
```

## 3. 레이어 관리 (Layer Management)

### 3.1 타일 레이어 (Tile Layer)
배경지도(Base Map)로 주로 사용됩니다.
```javascript
import XYZ from 'ol/source/XYZ';

const vworldLayer = new TileLayer({
  source: new XYZ({
    url: 'http://api.vworld.kr/req/wmts/1.0.0/KEY/Base/{z}/{y}/{x}.png'
  })
});
map.addLayer(vworldLayer);
```

### 3.2 벡터 레이어 (Vector Layer)
GeoJSON 등 데이터 기반의 피처를 렌더링할 때 사용합니다.
```javascript
import VectorLayer from 'ol/layer/Vector';
import VectorSource from 'ol/source/Vector';
import GeoJSON from 'ol/format/GeoJSON';
import { Circle as CircleStyle, Fill, Stroke, Style } from 'ol/style';

const vectorLayer = new VectorLayer({
  source: new VectorSource({
    url: 'data/seoul_districts.geojson',
    format: new GeoJSON()
  }),
  style: new Style({
    stroke: new Stroke({
      color: 'blue',
      width: 2
    }),
    fill: new Fill({
      color: 'rgba(0, 0, 255, 0.1)'
    })
  })
});
map.addLayer(vectorLayer);
```

## 4. 인터랙션 (Interactions)
사용자의 마우스/터치 동작에 반응하는 기능입니다.

### 4.1 선택 (Select)
```javascript
import Select from 'ol/interaction/Select';
import { click } from 'ol/events/condition';

const select = new Select({
  condition: click
});

map.addInteraction(select);

select.on('select', (e) => {
  if (e.selected.length > 0) {
    const feature = e.selected[0];
    console.log('Selected feature:', feature.getProperties());
  }
});
```

### 4.2 그리기 (Draw)
```javascript
import Draw from 'ol/interaction/Draw';

const draw = new Draw({
  source: vectorSource,
  type: 'Polygon' // Point, LineString, Polygon, Circle
});
map.addInteraction(draw);
```

## 5. 좌표계 변환 (Projections)
OpenLayers의 기본 좌표계는 `EPSG:3857` (Web Mercator)입니다.
GPS 좌표(`EPSG:4326`)를 사용할 때는 변환이 필요합니다.

```javascript
import { fromLonLat, toLonLat } from 'ol/proj';

// 경위도 -> Web Mercator
const mercatorCoord = fromLonLat([127.0, 37.0]);

// Web Mercator -> 경위도
const lonLatCoord = toLonLat(mercatorCoord);
```
