from openai import OpenAI
from common_utils.Config import Config
client = OpenAI(api_key=Config.OPENAI_API_KEY)


def HTMLFormatter(answer):

    try:
        print(answer)
        HTMLformaterPrompt = """
        You are a text formater who accepts text and Formats the given text as html. Do not use the text to answer questions, rather format the text as html and return the html.
        Do not add or modify text except format provided text as html.understand the text and add "\n" at relevant areas.
        examples:
            -> I am bill clinton and i am the president.\n based on the provided text what is my profession
            incorrect answer: <p>I am Bill Clinton and I am the President.</p>
                            <p>based on the provided text my profession is President.</p>

            correct answer: <p>I am Bill Clinton and I am the President.</p>
                            <p>based on the provided text what is my profession</p>

            -> to install sql. 1) download sql 2) click install button 3) select path 4) allocate memory 5) click done
                answer:    <p> to install sql. </p>
                        <ol>
                        <li>download sql</li>
                        <li>click install button</li>
                        <li>select path</li>
                        <li>allocate memory</li>
                        <li>click done</li>
                        </ol>

            """
        completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content":HTMLformaterPrompt },
            {"role": "user", "content": answer}
        ]
        )

        print(completion.choices[0].message.content)
        return completion.choices[0].message.content
    except Exception as exe:
        print("an error occured " +str(exe))

if __name__ == '__main__':
    answer = "hello how are you"
    print(HTMLFormatter(answer))