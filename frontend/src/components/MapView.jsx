import React, { useEffect, useRef } from 'react';
import 'ol/ol.css';
import Map from 'ol/Map';
import View from 'ol/View';
import TileLayer from 'ol/layer/Tile';
import OSM from 'ol/source/OSM';
import { fromLonLat } from 'ol/proj';

export default function MapView() {
    const mapRef = useRef();

    useEffect(() => {
        const map = new Map({
            target: mapRef.current,
            layers: [
                new TileLayer({
                    source: new OSM(),
                }),
            ],
            view: new View({
                center: fromLonLat([127.0246, 37.5326]), // Default Seoul
                zoom: 12,
            }),
        });

        return () => map.setTarget(null);
    }, []);

    return (
        <div className="flex-1 relative bg-slate-100">
            <div ref={mapRef} className="w-full h-full" />
            <div className="absolute top-6 left-6 z-10 bg-white/90 backdrop-blur shadow-lg p-6 rounded-2xl max-w-xs ring-1 ring-slate-200">
                <h2 className="text-lg font-bold text-slate-900 mb-2">현장 상황 지도</h2>
                <p className="text-sm text-slate-600 mb-4">프로젝트 현장의 위치와 실시간 데이터를 시각화합니다.</p>
                <div className="flex flex-col gap-2">
                    <div className="flex items-center gap-2 text-xs">
                        <span className="w-3 h-3 rounded-full bg-green-500" />
                        <span className="text-slate-700 font-medium">정상 운영 현장</span>
                    </div>
                    <div className="flex items-center gap-2 text-xs">
                        <span className="w-3 h-3 rounded-full bg-orange-500" />
                        <span className="text-slate-700 font-medium">관리 필요 현장</span>
                    </div>
                </div>
            </div>
        </div>
    );
}
