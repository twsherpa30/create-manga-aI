import {useState, useEffect} from 'react';

function MangaGame({manga, onNewManga}) {
    const [currentNodeId, setCurrentNodeId] = useState(null);
    const [currentNode, setCurrentNode] = useState(null)
    const [options, setOptions] = useState([])
    const [isEnding, setIsEnding] = useState(false)
    const [isWinningEnding, setIsWinningEnding] = useState(false)

    useEffect(() => {
        if (manga && manga.root_node) {
            const rootNodeId = manga.root_node.id
            setCurrentNodeId(rootNodeId)
        }
    }, [manga])
    useEffect(() => {
        if (currentNodeId && manga && manga.all_nodes) {
            const node = manga.all_nodes[currentNodeId]

            setCurrentNode(node)
            setIsEnding(node.is_ending)
            setIsWinningEnding(node.is_winning_endig)

            if (!node.is_ending && node.options && node.options.length > 0) {
                setOptions(node.options)
            } else {
                setOptions([])
            }
        }
    }, [currentNodeId, manga])


    const chooseOption = (optionId) => {
        setCurrentNodeId(optionId)
    }

    const restartManga = () => {
        if (manga && manga.root_node) {
            setCurrentNodeId(manga.root_node.id)
        }
    }

    return <div className="manga-game">
        <header className="manga-header">
            <h2>{manga.title}</h2>
        </header>

        <div className="manga-content">
            {currentNode && <div className="manga-node">
                <p>{currentNode.content}</p>

                {isEnding ?
                    <div className="manga-ending">
                        <h3>{isWinningEnding ? "Congratulations" : "The End"}</h3>
                        {isWinningEnding ? "You reached a winning ending" : "Your adventure has ended."}
                    </div>
                    :
                    <div className="manga-options">
                        <h3>What will you do?</h3>
                        <div className="options-list">
                            {options.map((option, index) => {
                                return <button
                                        key={index}
                                        onClick={() => chooseOption(option.node_id)}
                                        className="option-btn"
                                        >
                                        {option.text}
                                    </button>
                            })}
                        </div>
                    </div>
                }
            </div>}

            <div className="manga-controls">
                <button onClick={restartManga} className="reset-btn">
                    Restart Manga
                </button>
            </div>

            {onNewManga && <button onClick={onNewManga} className="new-manga-btn">
                New Manga
            </button>}

        </div>
    </div>
}

export default MangaGame