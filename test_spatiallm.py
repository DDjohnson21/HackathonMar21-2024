from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

def main():
    model_name = "manycore-research/SpatialLM-Llama-1B"
    
    # 1. Load tokenizer & model with trust_remote_code
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(model_name, trust_remote_code=True)
    
    # 2. Create a text-generation pipeline with the loaded model & tokenizer
    text_gen = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer
    )
    
    # 3. Simple test prompt
    prompt = "Who are you?"
    outputs = text_gen(prompt, max_length=50)
    print(outputs[0]["generated_text"])

if __name__ == "__main__":
    main()