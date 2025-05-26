
// Consola CMD Montevideo - Proyecto Base en React + Tailwind CSS
// Este archivo representa la estructura base del proyecto frontend

import { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { saveAs } from 'file-saver';
import * as XLSX from 'xlsx';

const temas = [
  'parque-eolico-1.jpg',
  'parque-eolico-2.jpg',
  'parque-eolico-3.jpg',
  'parque-eolico-4.jpg',
];

export default function ConsolaCMD() {
  const [mensajes, setMensajes] = useState([]);
  const [historial, setHistorial] = useState([]);
  const [temaActual, setTemaActual] = useState(temas[0]);

  useEffect(() => {
    const intervalo = setInterval(() => {
      const ahora = new Date();
      setMensajes((prev) => {
        const activos = [];
        const procesados = [];
        prev.forEach((m) => {
          const tiempo = new Date(m.timestamp);
          if ((ahora - tiempo) > 24 * 60 * 60 * 1000 || m.tipo === 'salida') {
            procesados.push(m);
          } else {
            activos.push(m);
          }
        });
        setHistorial((prevHist) => [...prevHist, ...procesados]);
        return activos;
      });
    }, 60000);
    return () => clearInterval(intervalo);
  }, []);

  const recibirMensaje = (nombre, texto, tipo) => {
    const timestamp = new Date().toISOString();
    const nuevoMensaje = { nombre, texto, tipo, timestamp };
    setMensajes((prev) => {
      if (tipo === 'salida') {
        const resto = prev.filter((m) => m.nombre !== nombre);
        setHistorial((prevHist) => [...prevHist, ...prev.filter((m) => m.nombre === nombre)]);
        return resto;
      }
      return [...prev, nuevoMensaje];
    });
  };

  const exportarExcel = () => {
    const hojaHistorial = XLSX.utils.json_to_sheet(historial);
    const hojaActivos = XLSX.utils.json_to_sheet(mensajes);
    const libro = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(libro, hojaHistorial, 'Historial');
    XLSX.utils.book_append_sheet(libro, hojaActivos, 'Activos');
    const wbout = XLSX.write(libro, { bookType: 'xlsx', type: 'array' });
    saveAs(new Blob([wbout], { type: 'application/octet-stream' }), 'cmd_montevideo.xlsx');
  };

  return (
    <div className="min-h-screen p-4" style={{ backgroundImage: `url(/fondos/${temaActual})`, backgroundSize: 'cover' }}>
      <header className="flex justify-between items-center mb-4">
        <img src="/logo_ute.png" alt="UTE" className="h-12" />
        <h1 className="text-xl font-bold text-white">Consola CMD Montevideo</h1>
        <Button onClick={exportarExcel}>Exportar a Excel</Button>
      </header>
      <Tabs defaultValue="activos">
        <TabsList>
          <TabsTrigger value="activos">Mensajes Activos</TabsTrigger>
          <TabsTrigger value="historial">Historial</TabsTrigger>
        </TabsList>
        <TabsContent value="activos">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {mensajes.map((msg, index) => (
              <Card key={index} className="bg-white/80">
                <CardContent>
                  <p><strong>{msg.nombre}</strong></p>
                  <p>{msg.texto}</p>
                  <p className="text-xs text-gray-600">{new Date(msg.timestamp).toLocaleString()}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>
        <TabsContent value="historial">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {historial.map((msg, index) => (
              <Card key={index} className="bg-white/60">
                <CardContent>
                  <p><strong>{msg.nombre}</strong></p>
                  <p>{msg.texto}</p>
                  <p className="text-xs text-gray-600">{new Date(msg.timestamp).toLocaleString()}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>
      </Tabs>
      <footer className="mt-8 text-white text-sm">
        Instrucciones: Ingresos y salidas deben estar bien redactados. No enviar mensajes fragmentados ni correcciones por separado.
      </footer>
    </div>
  );
}
