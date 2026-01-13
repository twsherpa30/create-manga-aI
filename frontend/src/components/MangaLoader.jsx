import {useState, useEffect} from 'react';
import {useParams, useNavigate} from "react-router-dom"
import axios from 'axios';
import LoadingStatus from './LoadingStatus.jsx';

import MangaGame from './MangeGame.jsx';
function MangaLoader() {
    const {id} = useParams();
    const navigate = useNavigate();
    const [manga, setManga] = useState(null);
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState(null);

    useEffect(() => {
        loadManga(id)
    }, [id])

    const loadManga = async (mangaId) => {
        setLoading(true)
        setError(null)

        try {
            const response = await axios.get(`/api/mangas/${mangaId}/complete`)
            setManga(response.data)
            setLoading(false)
        } catch (err) {
            if (err.response?.status === 404) {
                setError("Manga is not found.")
            } else {
                setError("Failed to load manga. Please try again later.")
            }
        } finally {
            setLoading(false)
        }
    }

    const createNewManga = () => {
        navigate("/")
    }

    if (loading) {
        return <LoadingStatus theme={"manga"} />
    }

    if (error) {
        return <div className="manga-loader">
            <div className="error-message">
                <h2>Manga Not Found</h2>
                <p>{error}</p>
                <button onClick={createNewManga}>Go to Manga Generator</button>
            </div>
        </div>
    }

    if (manga) {
        return <div className="manga-loader">
           <MangaGame manga={manga} onNewManga={createNewManga}></MangaGame>
        </div>
    }
}

export default MangaLoader;