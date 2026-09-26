
from rich.console import Console 
from rich.panel import Panel 
from rich.prompt import Prompt 
from rich.markdown import Markdown
from rich.align import Align 

import os
import json
import datetime
from dotenv import load_dotenv
from groq import Groq
from memory import messages, mem_clean, get_active_agent, agents, set_agent
from tools import available_tools, tools



load_dotenv()
console=Console()
client=Groq()
model= "openai/gpt-oss-120b"

line=("="*40)

def check_health():
    # 1. API KEY check
    api_key_ok = bool(os.getenv("GROQ_API_KEY"))
    api_status ="[green]Configured ✅[/green]" if api_key_ok else "[red]Missing ❌[/red]"

    # 2. Groq connection & model availability check
    model_ok = False
    try:
        active_models = [m.id for m in client.models.list().data]
        if model in active_models:
            model_ok =True
            model_status = f"[green]{model} ✅[/green]" 
        else:
            model_status = f"[red]{model} (Not Found) ⚠️[/red]"
    except Exception:
        model_status = f"[red]Connection Error ❌[/red]"


    # 3. Tools checck
    tools_ok = bool(available_tools)
    tools_status = f"[green]Connected ({len(available_tools)} tools) ✅[/green]" if tools_ok else "[red]No Tools ❌[/red]"


    # 4. Overall ststus check:
    if api_key_ok and model_ok and tools_ok:
        overall_status = "[bold green]Healthy 🟢[/bold green]"
    else:
        overall_status = "[bold red]Issue Detected 🔴[/bold red]"
    return api_status, model_status, tools_status, overall_status



api_status, model_status, tools_status, overall_status = check_health()

hero_screen = f"""
    [bold cyan]             Hey, this is 'ROLEX'[/bold cyan]
    [italic]              your AI Assistant[/italic]
    [bold cyan]--------------------------------------------   [/bold cyan]
        [bold white]Status:[yellow]
            • API KEY = {api_status}
            • MODEL   = {model_status}
            • TOOLS   = {tools_status}
            • OVERALL = {overall_status}[/yellow]
[dim]
Type '[yellow]/bye[/yellow]' or '[yellow]/quit[/yellow]' or '[yellow]/exit[/yellow]' to end this conversation[/dim]."""
    
console.print(Panel(Align.center(hero_screen), expand=True, border_style="bold cyan"))


# Session stats-க்காக variables
total_tokens_used = 0
prompt_tokens_used = 0
completion_tokens_used = 0


def main():
    global model, total_tokens_used, prompt_tokens_used, completion_tokens_used

    while True:
        user_input=Prompt.ask("[bold white]👨 YOU[/bold white]")

        if not user_input.strip():
            console.print(f"[bold red] === Ask anything... ===[/bold red]\n")
            continue

        if user_input.startswith("/"):
            if user_input.lower() in ["/exit", "/bye", "/quit", "/cls"]:
                console.print(f"[bold yellow]=== See you later..👋 ===[/bold yellow]")
                break

            if user_input == "/clear":
                chat_clear = mem_clean()
                console.print(f"[italic yellow]=== {chat_clear} ===[/italic yellow]\n")
                continue

            if user_input == "/save":
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

                folder_name = "chat_history"
                os.makedirs(folder_name, exist_ok=True)

                filename = os.path.join(folder_name, f"session_{timestamp}.md")
                with open(filename, "w", encoding="utf-8") as f:
                    f.write("# 🤖 Rolex AI Chat History\n\n")
                    for msg in messages:
                        if isinstance(msg, dict):
                            role = str(msg.get("role", "")).capitalize()
                            content = str(msg.get("content", ""))
                        else:
                            role = str(getattr(msg, "role", "")).capitalize()
                            content = str(getattr(msg, "role", ""))

                        if content and content != "None": 
                            f.write(f"### {role}\n{content}\n\n---\n\n")
                console.print(f"[bold green]=== Chat saved to '{filename}' 💾 ===[/bold green]\n")
                continue
            

            if user_input.startswith("/agent"):
                parts = user_input.split(maxsplit=1)
                if len(parts) > 1:
                    p_name=parts[1].strip()
                    result = set_agent(p_name)
                    console.print(f"[bold green]=== {result} 🎭 ===[/bold green]\n")
                else: 
                    available = ", ".join(agents.keys())
                    console.print(f"[bold yellow]Active Agent: {get_active_agent().capitalize()}[/bold yellow]")
                    console.print(f"[dim]Available Agent: {available}[/dim]")
                    console.print("[dim]Usage: /agent <name> (e.g., /agent coder)[/dim]\n")
                continue


            if user_input == "/models":
                c_models = [m.id for m in client.models.list().data]
                model_list = "\n".join([f"  [cyan][{i}][/cyan]    [yellow]{m_id}[/yellow]" for i, m_id in enumerate(c_models, 1)])
                console.print(Panel(
                    f"[bold cyan]Available Groq Models ({len(c_models)}):[/bold cyan]\n\n{model_list}",
                    title="[bold yellow]Groq Models[/bold yellow]",
                    expand=False,
                    border_style="yellow"
                ))
                while True:
                    user_choice = Prompt.ask("[bold white]Choose Model Number to change (press Enter to skip)[/bold white]", default="")
                    if user_choice.isdigit():
                        idx = int(user_choice) -1
                        if 0 <= idx < len(c_models):
                            model = c_models[idx]
                            console.print(f"[bold green]~~~~~~~~~~~~~~~~ Model changed to '{model}' ~~~~~~~~~~~~~~~~[/bold green]\n")
                            break
                        else:
                            console.print(f"[bold red]Please enter the number between '0' to '{len(c_models)}'[/bold red]")
                    else:
                        console.print("[bold red]Please enter the valid model number only.[/bold red]")      
                continue

            if user_input.startswith("/model"):
                parts = user_input.split(maxsplit=1)
                if len(parts) >1:
                    model = parts[1].strip()
                    console.print(f"[bold green]~~~~~~~~~~~~~~~~~~~~ Model changed to '{model}' ~~~~~~~~~~~~~~~~~~~~[/bold green]\n")
                    continue
                else:
                    console.print(f"[bold yellow]Current Model: {model}[/bold yellow]")
                    console.print("[dim]Usage: /model <model_name> (e.g., /model qwen/qwen3.8-27b)[/dim]\n")


            if user_input == "/stats":
                console.print(Panel(f"""[bold cyan]📊 Session Usage Statistics[/bold cyan]
• [yellow]Total Tokens Used:[/yellow] {total_tokens_used}
• [yellow]Prompt Tokens:[/yellow] {prompt_tokens_used}
• [yellow]Completion Tokens:[/yellow] {completion_tokens_used}
• [yellow]Active Model:[/yellow] {model}
""", expand=False, border_style="bold yellow"))
                continue


            if user_input == "/help":
                console.print(Panel(f"""[bold yellow]{line}\nCommands:\n{line}[/bold yellow]
End Session           /exit, /bye, /quit
Clear memory          /clear
Save Conversation     /save
Change/View Model     /model <model_name>
Usage Stats           /stats
Help                  /help
""", expand=False, border_style="bold yellow"))

            else:
                console.print(f"[bold red]=== Unknown command '{user_input}' ===[/bold red]\n")
            continue

        else:
            messages.append({"role":"user", "content": user_input})
            with console.status("[dim]Thinking...[/dim]", spinner="dots", spinner_style="dim"):
                response = client.chat.completions.create(
                    model=model,
                    messages=messages,
                    tools=tools,
                    tool_choice="auto",
                    temperature=0.7
                )

            if response.usage:
                total_tokens_used += response.usage.total_tokens
                prompt_tokens_used += response.usage.prompt_tokens 
                completion_tokens_used += response.usage.completion_tokens 
        
            ##################### LLM first response ###################
            console.print(Panel(f"[italic dim]{response}[/italic dim]", title="llm Responses", border_style="dim"))

            current_response = response.choices[0].message
            llm_response=current_response.content

            while current_response.tool_calls:
                messages.append(current_response)

                for tool_call in current_response.tool_calls:
                    tool_name = tool_call.function.name
                    tool_to_call = available_tools.get(tool_name)
                    tool_args = json.loads(tool_call.function.arguments)
                    tool_args = {k: v for k, v in tool_args.items() if k != ""}

                    if tool_to_call:
                        try:
                            tool_output = tool_to_call(**tool_args) if tool_args else tool_to_call()
                        except TypeError:
                            tool_output = tool_to_call()

                        messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "name": tool_name,
                            "content": str(tool_output), 
                        })
                    
                        console.print(Panel(f"[italic dim]Tool Name:  {tool_name}\nArguments:  {tool_args}\nTool Output:  {tool_output}[/italic dim]", title= "Tool Calling", expand=True, border_style="dim"))

                    else:
                        messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "name": tool_name,
                            "content": f"Error: Tool '{tool_name}' not found.",
                        })
                        

                next_response=client.chat.completions.create(
                    model=model,
                    messages=messages,
                    tools=tools,
                    tool_choice="auto",
                    temperature=0.7
                )
                ##################### LLM response with tool output ###################
                #console.print(Panel(f"[italic dim]{next_response}[/italic dim]", title="llm Responses with Tool output", border_style="dim"))

                if next_response.usage:
                    total_tokens_used += next_response.usage.total_tokens
                    prompt_tokens_used += next_response.usage.prompt_tokens 
                    completion_tokens_used += next_response.usage.completion_tokens

                current_response = next_response.choices[0].message
                
            sub_details=f" [white]Total Tokens Used:[/white] {total_tokens_used} | [white]Active Agent:[/white] {get_active_agent().capitalize()}  | [white]Active Model:[/white] {model}"
            final_response = f"{current_response.content}"
            
            console.print(
                Panel(
                    Markdown(final_response or ""), 
                    title=f"[bold Yellow]🤖 {get_active_agent().upper()}[/bold Yellow]",
                    subtitle=f"[yellow dim]{sub_details}[/yellow dim]",  # ✅ subtitle-ஆக மாற்றப்பட்டுள்ளது
                    title_align="left", 
                    subtitle_align="right", 
                    border_style="cyan"
                )
            )


            messages.append({"role":"assistant", "content": final_response})
            print("\n")

            ##################### chat memory ###################
            #console.print(Panel(f"[italic dim]{messages}[/italic dim]", title="Chat Memory", border_style="dim"))

if __name__== "__main__":
    main()