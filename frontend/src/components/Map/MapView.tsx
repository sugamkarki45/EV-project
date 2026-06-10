import React, { useEffect, useRef } from 'react';
import maplibregl from 'maplibre-gl';
import 'maplibre-gl/dist/maplibre-gl.css';

interface MapViewProps {
  onPinClick?: (listingId: string) => void;
}

const MapView: React.FC<MapViewProps> = ({ onPinClick }) => {
  const mapContainer = useRef<HTMLDivElement>(null);
  const map = useRef<maplibregl.Map | null>(null);

  useEffect(() => {
    if (map.current) return;
    if (!mapContainer.current) return;

    map.current = new maplibregl.Map({
      container: mapContainer.current,
      style: {
        version: 8,
        sources: {
          'osm': {
            type: 'raster',
            tiles: ['https://tile.openstreetmap.org/{z}/{x}/{y}.png'],
            tileSize: 256,
            attribution: '&copy; OpenStreetMap contributors'
          }
        },
        layers: [
          {
            id: 'osm-layer',
            type: 'raster',
            source: 'osm'
          }
        ]
      },
      center: [85.324, 27.717], // Kathmandu
      zoom: 13
    });

    map.current.addControl(new maplibregl.NavigationControl());

    // Mock markers for demo
    const markers = [
      { id: '1', lat: 27.717, lng: 85.324, type: 'hotel' },
      { id: '2', lat: 27.720, lng: 85.330, type: 'home' }
    ];

    markers.forEach(m => {
      const el = document.createElement('div');
      el.className = 'marker';
      el.style.backgroundColor = m.type === 'hotel' ? '#8B5CF6' : '#3B82F6';
      el.style.width = '20px';
      el.style.height = '20px';
      el.style.borderRadius = '50%';
      el.style.cursor = 'pointer';

      new maplibregl.Marker(el)
        .setLngLat([m.lng, m.lat])
        .addTo(map.current!)
        .getElement()
        .addEventListener('click', () => onPinClick?.(m.id));
    });

  }, [onPinClick]);

  return <div ref={mapContainer} className="w-full h-full" />;
};

export default MapView;
