import {useState,useEffect} from "react"
import { listTickets,updateTicket } from "./api"

const STATUS_OPTIONS=["open","in_progress","resolved"]

export default function TicketList({refreshKey}){ 
    const [tickets,setTickets] = useState([])
    const [statusFilter,setStatusFilter] = useState("")
    const [loading,setLoading] = useState(true)

    async function fetchTickets(){
        setLoading(true);
        const params= statusFilter? {status:statusFilter} :{};
        const res=await listTickets(params); // when this runs when status filter changes then it only fetches data with that status
        setTickets(res.data)
        setLoading(false);
    }

    useEffect(()=>{
        fetchTickets();
    },[statusFilter,refreshKey]);

    async function handleStatusChange(id,newStatus){
        setTickets((prev)=> prev.map((t)=>{
            return t.id ===id? {...t,status:newStatus} :t
        }));

        await updateTicket(id,{status:newStatus}); //// when this runs when status filter changes it updates status for that ticket
    }


return (
    <div>
        <h2>Tickets</h2>
        <label>
            Filter by status:{" "}
            <select value={statusFilter} 
            onChange={(e)=>setStatusFilter(e.target.value)}>
                <option value="">All</option>
                {
                    STATUS_OPTIONS.map((s)=>(
                        <option key={s} value={s}>{s}</option>
                    ))
                }
            </select>
        </label>

        {loading?(
            <p>Loading...</p>
        ):(
            <table style={{width:"100%",marginTop:"1rem", borderCollapse:"collapse"}}>
                <thead>
                    <tr style={{textAlign: "left",borderBottom: "1px solid #ccc" }}>
                        <th>Title</th>
                        <th>Category</th>
                        <th>Priority</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    {tickets.map((t)=>(
                        <tr key={t.id} style={{ borderBottom: "1px solid #eee" }}>
                            <td>{t.title}</td>
                            <td>{t.category}</td>
                            <td>{t.priority}</td>
                            <td>
                                <select value={t.status} onChange={(e)=> handleStatusChange(t.id,e.target.value)}>
                                    {
                                        STATUS_OPTIONS.map((s)=>(
                                            <option key={s} value={s}>{s}</option>
                                        ))
                                    }
                                </select>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        )}
    </div>
)
}