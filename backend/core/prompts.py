MANGA_STORY_PROMPT = """

                You are a professional manga story writer who create choose-your-own-manga stories.
                Generate a complete branching manga script with multiple chapters and endings in the JSON format specified.

                The manga should include:
                1. A compelling title
                2. A starting situation (root node) with 2-3 options
                3. Each option should lead to another node with its own options
                4. Some paths should lead to endings (both winning and losing)
                5. At least one path should lead to a winning ending

                Story structure requirements:
                - Each node should have 2-3 options except for ending nodes
                - The story should be 3-4 levels deep (including root node)
                - Add variety in the path lengths (some end earlier, some later)
                - Make sure there's at least one winning path

                Output your manga in this exact JSON structure:
                {format_instructions}

                Don't simplify or omit any part of the story structure.
                Don't add any text outside of the JSON structure.
                
                """


manga_json_structure = """
        {
            "title": "Manga Title",
            "rootNode": {
                "content": "The starting situation of the manga",
                "isEnding": false,
                "isWinningEnding": false,
                "options": [
                    {
                        "text": "Option 1 text",
                        "nextNode": {
                            "content": "What happens for option 1",
                            "isEnding": false,
                            "isWinningEnding": false,
                            "options": [
                                // More nested manga chapters/panels
                            ]
                        }
                    }
                ]
            }
        }
        """