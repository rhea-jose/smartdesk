import { useState } from "react";
import TicketForm from "./TicketForm";
import TicketList from "./TicketList";

export default function App() {
  const [refreshKey, setRefreshKey] = useState(0);

  return (
    <div style={{ maxWidth: "800px", margin: "0 auto", padding: "2rem", fontFamily: "sans-serif" }}>
      <h1>SmartDesk</h1>
      <TicketForm onCreated={() => setRefreshKey((k) => k + 1)} />
      <TicketList refreshKey={refreshKey} />
    </div>
  );
}