from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import difflib

app = Flask(__name__)
CORS(app)


responses = {
    "what is systemic altruism": "Systemic altruism focuses on addressing the root causes of social issues through sustainable solutions.",
    "how can i contribute": "You can contribute by supporting organizations, volunteering, and advocating for systemic changes.",
    "examples of systemic altruism": "Examples include policy reforms, educational programs, and healthcare accessibility initiatives.",
    "what are the key principles of systemic altruism": "Key principles include sustainability, equity, evidence-based approaches, and collaboration.",
    "how does systemic altruism differ from traditional charity": "Traditional charity often addresses symptoms, whereas systemic altruism targets root causes to create long-term impact.",
    "why is systemic altruism important": "It ensures that social change efforts have long-term, meaningful, and scalable impacts.",
    "what are some effective systemic altruism projects": "Effective projects include healthcare accessibility reforms, climate change mitigation policies, and educational equity initiatives.",
    "how can businesses adopt systemic altruism": "Businesses can adopt systemic altruism by aligning their corporate social responsibility (CSR) initiatives with sustainable and systemic goals.",
    "how do governments support systemic altruism": "Governments can support systemic altruism through policy reforms, funding initiatives, and promoting public-private partnerships.",
    "what are the biggest challenges in systemic altruism": "Challenges include resource allocation, political resistance, and measuring long-term impact.",
    "how does systemic altruism address poverty": "It addresses poverty by focusing on structural inequalities, access to education, and economic opportunities.",
    "who are the key stakeholders in systemic altruism": "Stakeholders include governments, non-profits, businesses, academic institutions, and local communities.",
    "how can systemic altruism improve healthcare": "By advocating for universal healthcare access, policy reforms, and better resource distribution.",
    "what is the role of education in systemic altruism": "Education plays a key role by empowering individuals, creating awareness, and fostering critical thinking for sustainable solutions.",
    "can systemic altruism solve climate change": "It provides long-term solutions through policy advocacy, sustainable business practices, and community-led initiatives.",
    "what is altruism": "Altruism refers to the selfless concern for the well-being of others.",
    "why do people practice altruism": "People practice altruism for ethical reasons, personal fulfillment, or social responsibility.",
    "how can altruism improve society": "Altruism fosters a sense of community, reduces inequality, and promotes collective well-being.",
    "what are some examples of altruistic behavior": "Volunteering, donating to charity, and helping a stranger in need are common examples.",
    "is altruism innate or learned": "Studies suggest that altruism can be both an innate human trait and a learned behavior influenced by culture and upbringing.",
    "what is the difference between altruism and philanthropy": "Philanthropy typically involves financial contributions, while altruism encompasses a broader range of selfless acts.",
    "how can I encourage altruism in my community": "You can encourage altruism by organizing community events, volunteering, and raising awareness.",
    "what are the psychological benefits of altruism": "Practicing altruism can improve mental well-being, reduce stress, and enhance social connections.",
    "how do systemic solutions benefit society": "They create long-term, sustainable impacts by addressing social challenges at their root.",
    "how can systemic altruism address inequality": "Through policies that promote equal opportunities, access to education, and economic empowerment.",
    "what are some organizations promoting systemic altruism": "Organizations like Effective Altruism, GiveWell, and Open Philanthropy promote systemic change.",
    "how can technology support systemic altruism": "Technology can enable data-driven decision-making, resource optimization, and greater transparency.",
    "what policies support systemic altruism": "Policies focusing on healthcare access, education reform, and environmental sustainability support systemic altruism.",
    "how can systemic altruism improve mental health support": "By advocating for mental health policies, funding, and community-based interventions.",
    "what is the economic impact of systemic altruism": "Systemic altruism can lead to long-term economic growth by addressing foundational social issues.",
    "who founded systemic altruism": "Systemic altruism is an evolving concept inspired by various philanthropic and economic theories.",
    "how do I get started with systemic altruism": "You can start by educating yourself, supporting relevant causes, and participating in advocacy programs.",
    "what are the ethical considerations of systemic altruism": "Ethical considerations include fairness, accountability, and respect for community needs.",
    "is systemic altruism cost-effective": "Yes, when applied strategically, it can provide high returns on social investments.",
    "hello": "Hi there! How can I assist you with systemic altruism today?",
    "hi": "Hello! Feel free to ask me anything about systemic altruism.",
    "thanks": "You're welcome! Let me know if you have more questions.",
    "thank you": "You're welcome! Always here to help.",
    "default": "Sorry, I don't understand. Could you please rephrase your question?",
}

def get_bot_response(user_message):
   
    
    user_message = user_message.lower()
    
   
    if user_message in responses:
        return responses[user_message]
    
   
    for key in responses:
        if key in user_message:
            return responses[key]
    
   
    return "I'm not sure how to respond to that. Could you try rephrasing or ask me something else?"

def get_best_match(user_message):
    questions = list(responses.keys())
    closest_match = difflib.get_close_matches(user_message, questions, n=1, cutoff=0.6)  # Adjust 
    return closest_match[0] if closest_match else None

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        user_message = get_best_match(user_message)
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        response = get_bot_response(user_message)
        return jsonify({'response': response})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 