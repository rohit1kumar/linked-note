# LinkedIn Connections Message Generator

### How to use:

1. Clone the repo & update the `.env` file

   ```bash
   git clone https://github.com/rohit1kumar/linkedin-msg-gen.git
   cd linkedin-msg-gen
   cp .env.example .env
   ```

2. (Optional) Use Docker:

   ```bash
   docker-compose up --build
   ```

3. (if not using Docker) Install dependencies & run:

   ```bash
   pip install -r requirements.txt
   playwright install chromium
   python app/main.py
   ```

4. Go to `http://localhost:5000` in your browser for using UI or use the API directly.

### API Request & Response:

- Request:

  ```
  curl --location 'http://127.0.0.1:5000/create_message' \
  --header 'Content-Type: application/json' \
  --data-raw '{
      "username": "john@gmail.com",
      "password": "my_password",
      "profile_url": "https://www.linkedin.com/in/johnDoe",
  }'
  ```

- Response:

  ```json
  {
  	"connection_message": "Hello John, I'm impressed by your work, Would love to connect and discuss potential collaborations in the future. Best regards.",
  	"profile_data": {
  		"headline": "Forbes 30u30 | Co-Founder @ABC",
  		"name": "John Doe",
  		"posts": ["This is a post", "This is another post"]
  	}
  }
  ```

### Cost of Running:

Under following assumptions:

- Model: `gpt-4o-mini`
- Each post container contains 400 tokens
- Each prompt + user details costs 60 extra tokens
- The average message output is 50 tokens

Then the input token would be:

- `400 * 5 + 60 + 50 = 2110 tokens`

According to [gptforwork.com](https://gptforwork.com/tools/openai-chatgpt-api-pricing-calculator), for my case the price per API call is $0.0003.

For running 30 days with 5 calls per day (150 calls total), the total cost would be:

- `30*5*0.0003 = $0.045` per month
