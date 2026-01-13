function LoadingStatus({theme}) {
    return <div className="loading-container">
        <h2>Generating Your {theme} Manga </h2>

        <div className="loading-animation">
            <div className="spinner"></div>
        </div>

        <p className="loading-info">
            Please wait while we generate your manga...
        </p>
    </div>
}

export default LoadingStatus;