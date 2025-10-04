import { useEffect, useState } from "react";
import Papa from "papaparse";

export default function MapView() {
  const [data, setData] = useState([]);

  useEffect(() => {
    Papa.parse("/data/bloomwatch_land.csv", {
      download: true,       // fetch CSV from public folder
      header: true,         // first row as keys
      dynamicTyping: true,  // convert numbers automatically
      worker: true,         // parse in web worker for big files
      step: function (row) {
        // Optionally process row by row
      },
      complete: function (results) {
        setData(results.data);
        console.log("Loaded", results.data.length, "rows");
      },
    });
  }, []);

  return <div>Loaded {data.length} rows</div>;
}
