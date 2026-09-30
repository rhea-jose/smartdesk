import {useState} from "react"
import { createTicket } from "./api"

export default function TicketForm({onCreated}){
    const [title,setTitle]= useState("");
    const [description,setDescription] = useState("");
    const [submitting,setSubmitting]= useState(false);
    const [error,setError]= useState(null);

    async function handleSubmit(e){
        e.preventDefault();
        setSubmitting(true);
        setError(null);
        try{
            const res= await createTicket({title,description});
            onCreated(res.data);
            setTitle("");
            setDescription("");
        } catch(err){
            setError("Could not submit ticket. Please try again")
        } finally{
            setSubmitting(false);
        }
    }


return (
    <form onSubmit={handleSubmit} style={{marginBotton:"2rem"}}>
        <h2>Submit a Ticket</h2>
        <div>
            <label>Title</label><br/>
            <input value={title} onChange={(e)=> setTitle(e.target.value)} 
            minLength={3} required style={{width:"100%"}}></input>
        </div>
        <div>
            <label>Description</label> <br/>
            <textarea value={description} 
            onChange={(e)=>setDescription(e.target.value)} minLength={5}
            required rows={4} style={{ width: "100%" }}></textarea>
        </div>
        {
            error&& <p style={{color:"red"}}>{error}</p>
        }
        <button type="submit" disabled={submitting}>
            {submitting? "Submitting": "Submit"}
        </button>
    </form>
)
}