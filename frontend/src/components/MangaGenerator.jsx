import {useState, useEffect} from "react"
import {useNavigate} from "react-router-dom";
import axios from "axios";
import ThemeInput from "./ThemeInput.jsx";
import LoadingStatus from "./LoadingStatus.jsx";



function MangaGenerator() {
    const navigate = useNavigate()
    const [theme, setTheme] = useState("")
    const [jobId, setJobId] = useState(null)
    const [jobStatus, setJobStatus] = useState(null)
    const [error, setError] = useState(null)
    const [loading, setLoading] = useState(false)

    useEffect(() => {
        let pollInterval;

        if (jobId && jobStatus === "processing") {
            pollInterval = setInterval(() => {
                pollJobStatus(jobId)
            }, 5000)
        }

        return () => {
            if (pollInterval) {
                clearInterval(pollInterval)
            }
        }
    }, [jobId, jobStatus])

    const generateManga = async (theme) => {
        setLoading(true)
        setError(null)
        setTheme(theme)

        try {
            const response = await axios.post(`/api/mangas/create`, {theme})
            const {job_id, status} = response.data
            setJobId(job_id)
            setJobStatus(status)

            pollJobStatus(job_id)
        } catch (e) {
            setLoading(false)
            setError(`Failed to generate manga: ${e.message}`)
        }
    }

    const pollJobStatus = async (id) => {
        try {
            const response = await axios.get(`/api/jobs/${id}`)
            const {status, manga_id, error: jobError} = response.data
            setJobStatus(status)

            if (status === "completed" && manga_id) {
                fetchManga(manga_id)
            } else if (status === "failed" || jobError) {
                setError(jobError || "Failed to generate manga")
                setLoading(false)
            }
        } catch (e) {
            if (e.response?.status !== 404) {
                setError(`Failed to check manga status: ${e.message}`)
                setLoading(false)
            }
        }
    }

    const fetchManga = async (id) => {
        try {
            setLoading(false)
            setJobStatus("completed")
            navigate(`/manga/${id}`)
        } catch (e) {
            setError(`Failed to load manga: ${e.message}`)
            setLoading(false)
        }
    }

    const reset = () => {
        setJobId(null)
        setJobStatus(null)
        setError(null)
        setTheme("")
        setLoading(false)
    }

    return <div className="manga-generator">
        {error && <div className="error-message">
            <p>{error}</p>
            <button onClick={reset}>Try Again</button>
        </div>}

        {!jobId && !error && !loading && <ThemeInput onSubmit={generateManga}/>}

        {loading && <LoadingStatus theme={theme} />}
    </div>
}

export default MangaGenerator;

