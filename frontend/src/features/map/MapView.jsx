import React, { useEffect, useRef } from 'react';
import 'ol/ol.css';
import Map from 'ol/Map';
import View from 'ol/View';
import TileLayer from 'ol/layer/Tile';
import OSM from 'ol/source/OSM';
import { fromLonLat } from 'ol/proj';
import { MapPin, Navigation, Layers } from 'lucide-react';

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
        <div className="relative w-full h-[70vh] rounded-[40px] overflow-hidden shadow-2xl border border-slate-200 animate-in zoom-in-95 duration-700">
            <div ref={mapRef} className="w-full h-full" />

            {/* Map Overlay UI */}
            <div className="absolute top-8 left-8 z-10 space-y-4">
                <div className="bg-white/90 backdrop-blur-xl shadow-2xl p-6 rounded-[32px] max-w-xs ring-1 ring-slate-200/50">
                    <div className="flex items-center gap-3 mb-3">
                        <div className="p-2 bg-primary-600 rounded-2xl">
                            <MapPin className="w-5 h-5 text-white" />
                        </div>
                        <h2 className="text-lg font-black text-slate-900">현장 공간 데이터</h2>
                    </div>
                    <p className="text-xs text-slate-500 leading-relaxed mb-6">
                        OpenLayers를 활용한 위성지도 및 레이어 중첩 예제입니다. 실제 현장 데이터를 시각화해 보세요.
                    </p>

                    <div className="space-y-3">
                        <div className="flex items-center justify-between p-3 bg-slate-50 rounded-2xl group hover:bg-slate-100 transition-colors cursor-pointer border border-transparent hover:border-slate-200">
                            <div className="flex items-center gap-3">
                                <Navigation className="w-4 h-4 text-primary-500" />
                                <span className="text-xs font-bold text-slate-700">위치 이동</span>
                            </div>
                            <span className="text-[10px] text-slate-400">Ctrl + L</span>
                        </div>
                        <div className="flex items-center justify-between p-3 bg-slate-50 rounded-2xl group hover:bg-slate-100 transition-colors cursor-pointer border border-transparent hover:border-slate-200">
                            <div className="flex items-center gap-3">
                                <Layers className="w-4 h-4 text-primary-500" />
                                <span className="text-xs font-bold text-slate-700">레이어 설정</span>
                            </div>
                            <span className="text-[10px] text-slate-400">Ctrl + Z</span>
                        </div>
                    </div>
                </div>
            </div>

            {/* Bottom Status Bar */}
            <div className="absolute bottom-8 left-1/2 -translate-x-1/2 z-10 px-6 py-3 bg-slate-900/90 backdrop-blur text-white rounded-full flex gap-6 text-xs font-bold shadow-2xl ring-1 ring-white/20">
                <div className="flex items-center gap-2">
                    <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
                    <span>정상 연결됨</span>
                </div>
                <div className="w-px h-3 bg-white/20" />
                <span>EPSG:3857 (Web Mercator)</span>
            </div>
        </div>
    );
}
