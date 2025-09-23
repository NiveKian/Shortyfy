import { useState } from "react"
import { useNavigate } from "react-router-dom"
import { checkURL , checkHTTP} from "../util/tools";
import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

interface ShortenResponse {
  short_url: string
}

export const Home = () => {

  const [url, setUrl] = useState("")
  const navigate = useNavigate()

  const handleSubmit = async () => {
    try {

      if (!checkURL(url)) throw new Error("O Link inserido não é valido!")

      const checked_url = checkHTTP(url)

      const response = await fetch("http://localhost:8000/shorten", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: checked_url }),
      })

      if (!response.ok) throw new Error("Erro ao encurtar o link!")

      const data = (await response.json()) as ShortenResponse
      navigate("/result", { state: { shortUrl: data.short_url } })

    } catch (err: any) {
      toast.error("Error trying to fetch API", {
        position: "top-right",
        theme: 'colored'
      });
    }
  }

  return (
    <div className="flex flex-col items-center justify-center min-w-screen gap-6 px-4">

      <div className="flex justify-center py-8 mb-10 gap-4">
        <h1 className="text-5xl lg:text-6xl font-bold">
          <span className="text-white drop-shadow-lg">Shorty</span>
          <span className="text-green-400 drop-shadow-lg">Fy</span>
        </h1>
      </div>

      <div className="flex justify-center items-center gap-4 px-4 w-full">
        <input
          type="text"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="Copy your text here"
          className="w-full max-w-3xl  bg-white/5 border border-white/10 rounded px-4 py-3 text-white transition focus:outline-none focus:border-green-400 focus:bg-red-500/5"
        />
      </div>

      <div className="flex flex-row justify-center items-center gap-4">
        <button
          onClick={handleSubmit}
          className="bg-green-500 hover:bg-green-800 text-white px-4 py-2 rounded text-xl font-bold"
        >
          Generate Link
        </button>
      </div>
      <ToastContainer aria-label={undefined} />
    </div>
  )
}