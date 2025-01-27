# Systemic Altruism Chatbot

This is a chatbot application built with **React** for the frontend and **Flask** for the backend. The chatbot provides information about systemic altruism and answers user queries by fetching predefined responses or dynamic information from various sources, including web scraping and an integration with Hugging Face's AI models.

## Features

- **Real-time queries:** The chatbot can fetch real-time data from specific pages and provide answers based on current information.
- **Predefined responses:** The chatbot can also respond with static, predefined answers from a JSON file.
- **Hugging Face Integration:** Utilizes the Hugging Face API to generate conversational AI responses.
- **Selenium Web Scraping:** Scrapes data from a Notion page to provide dynamic content for specific queries.
- **User-friendly interface:** The chatbot is designed to be intuitive, with a clean user interface for interacting with the bot.

## Tech Stack

### Backend:
- **Flask**: A lightweight web framework for Python.
- **Hugging Face API**: For generating AI responses based on user input.
- **Selenium + BeautifulSoup**: For scraping real-time data from a Notion page.
- **dotenv**: To manage environment variables like the Hugging Face API key.
- **Requests**: For making HTTP requests.
- **Logging**: To log information and errors for debugging.

### Frontend:
- **React**: JavaScript library for building the user interface.
- **Axios**: To make HTTP requests to the Flask backend.
- **CSS**: For styling the chatbot interface.

## Installation

### Backend (Flask)

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/systemic-altruism-chatbot.git
    cd systemic-altruism-chatbot/backend
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Set up environment variables by creating a `.env` file and adding the following:

    ```plaintext
    HF_API_KEY=your_hugging_face_api_key
    ```

4. Run the Flask server:

    ```bash
    python app.py
    ```

    The backend will be running at `http://127.0.0.1:5000`.

### Frontend (React)

1. Navigate to the frontend folder:

    ```bash
    cd ../frontend
    ```

2. Install dependencies:

    ```bash
    npm install
    ```

3. Run the React app:

    ```bash
    npm start
    ```

    The frontend will be accessible at `http://localhost:3000`.

## Usage

- When you open the chatbot interface, it will greet you with a default message.
- You can type a message in the input box and press **Enter** or click **Send** to send the message to the backend.
- The backend will either return a predefined response or fetch real-time data from the Notion page and respond with relevant information.
- The chatbot can also generate AI-powered responses using the Hugging Face API.

## API Endpoints

### `POST /chat`
- **Description**: Accepts a user message and returns a chatbot response.
- **Request Body**:
    ```json
    {
        "message": "Your user message here"
    }
    ```
- **Response**:
    ```json
    {
        "response": "Chatbot's response here"
    }
    ```

## Deployment

- To deploy the backend, you can use platforms like **Heroku**, **Render**, or **AWS** to host the Flask application.
- The frontend can be deployed on **GitHub Pages**, **Netlify**, or **Vercel** for easy hosting.

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- Hugging Face for their conversational AI models.
- Selenium and BeautifulSoup for web scraping.
- Flask and React for the web application stack.
