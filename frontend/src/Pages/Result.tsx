import { useNavigate } from "react-router-dom"
import { useLocation } from "react-router-dom";
import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

interface LocationState {
  shortUrl: string
}

export const Result = () => {

  const navigate = useNavigate()
  const location = useLocation()
  const state = location.state as LocationState | null;
  const shortUrl = state?.shortUrl

  const handleCopy = () => {
    if (!shortUrl) return;
    navigator.clipboard.writeText(shortUrl)
    toast.success("Link Copiado!", {
      position: "top-right",
      theme: "colored",
    });
  }

  const openLink = () => {
    if (!shortUrl) navigate("/");
    window.open(shortUrl, "_blank")
  }

  return (

    <div className="flex flex-col items-center justify-center min-w-screen gap-6 px-4">

      <div className="flex justify-center py-8 mb-10 gap-4">
        <h1 className="text-4xl sm:text-4xl md:text-5xl lg:text-6xl font-bold">
          <span className="text-white drop-shadow-lg">Shorty</span>
          <span className="text-green-400 drop-shadow-lg">Fy</span>
        </h1>
      </div>

      <div className="flex justify-center items-center gap-4 px-4 w-full">
        <input
          readOnly
          type="text"
          value={shortUrl}
          className="w-full max-w-3xl bg-red-500/5 border-red-400 rounded px-4 py-3 text-white transition outline-none focus:border-red-400 text-lg text-center shadow-sm"
        ></input>
      </div>

      <div className="flex flex-row justify-center items-center gap-4">
        <button
          onClick={handleCopy}
          className="bg-red-500 hover:bg-red-800 text-white px-4 py-2 rounded text-xl font-bold"
        >
          Copy
        </button>

        <button
          onClick={openLink}
          className="bg-green-500 hover:bg-green-800 text-white px-4 py-2 rounded text-xl font-bold"
        >
          Redirect
        </button>
      </div>
      <ToastContainer aria-label={undefined} />
    </div>
  )
}