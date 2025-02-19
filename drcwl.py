import itertools
import argparse
import os
import time
import concurrent.futures
from rich.console import Console
from rich.progress import Progress
from rich.text import Text


console = Console()

def print_banner():
    banner = Text("""                                      
    //    ) )     //   ) )     //   ) ) 
   //    / /     //___/ /     //        
  //    / /     / ___ (      //         
 //    / /     //   | |     //          
//____/ /     //    | |    ((____/ /    
                                   
""", style="blue")

    console.print(banner)
    console.print("[bold cyan]🚀 Welcome to DRC Wordlist Generator! 🔥[/bold cyan]")

def validate_input(min_length, max_length, charset):
    if min_length <= 0 or max_length <= 0:
        raise ValueError("Word lengths must be positive integers.")
    if min_length > max_length:
        raise ValueError("Minimum length cannot be greater than maximum length.")
    if not charset:
        raise ValueError("Character set cannot be empty.")
    if len(set(charset)) != len(charset):  
        raise ValueError("Character set contains duplicate characters.")
    return True

def get_predefined_charset(option):
    charsets = {
        'alpha': 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ',
        'alphanumeric': 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',
        'digits': '0123456789',
        'special': '!@#$%^&*()_+[]{}|;:,.<>?/~`',
        'lower': 'abcdefghijklmnopqrstuvwxyz',
        'upper': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    }
    return charsets.get(option, None)

def generate_wordlist_for_length(charset, length, prefix, suffix):
    """Yield generated words one by one instead of creating a list."""
    for word in itertools.product(charset, repeat=length):
        yield prefix + "".join(word) + suffix

def generate_wordlist(charset, min_length, max_length, prefix, suffix, output_file, limit, threads):
    count = 0
    total_words = sum(len(charset) ** length for length in range(min_length, max_length + 1))
    total_words = min(total_words, limit) if limit else total_words

    # Warn if wordlist is large
    if total_words > 1000000:
        console.print("[bold yellow]Warning: This is a large wordlist. It may take some time to generate.[/bold yellow]")

    # Initialize progress bar and start time
    start_time = time.time()

    try:
        with open(output_file, "w") as file:
            with Progress() as progress:
                task = progress.add_task("[bold cyan]⚡ Generating words...", total=total_words)

                # Use a ThreadPoolExecutor for parallel processing
                with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
                    futures = []

                    # Submit tasks for each length
                    for length in range(min_length, max_length + 1):
                        futures.append(executor.submit(generate_wordlist_for_length, charset, length, prefix, suffix))

                    # Write the generated words to the file
                    for future in concurrent.futures.as_completed(futures):
                        for word in future.result():
                            if limit and count >= limit:
                                console.print(f"\n[green]✔ Wordlist limit reached: {limit} words saved.[/green]")
                                return
                            file.write(word + "\n")
                            count += 1
                            progress.update(task, advance=1)

            elapsed_time = time.time() - start_time
            console.print(f"\n[bold green]✔ Wordlist saved to {output_file} with {count} words.[/bold green] 🎉")
            console.print(f"[bold cyan]Elapsed time: {elapsed_time:.2f} seconds.[/bold cyan]")

    except KeyboardInterrupt:
        console.print("\n[bold red]⚠ Generation interrupted by user. Exiting...[/bold red]")
        return
    except Exception as e:
        console.print(f"[bold red]Error: {e}[/bold red]")
        return


def print_wordlist_description(charset, min_length, max_length, prefix, suffix, threads):
    charset_desc = f"Charset used: {charset}\n"
    length_desc = f"Word lengths: {min_length} to {max_length}\n"
    prefix_desc = f"Prefix: {prefix}\n" if prefix else "No prefix\n"
    suffix_desc = f"Suffix: {suffix}\n" if suffix else "No suffix\n"
    threads_desc = f"Using {threads} threads for generation.\n"
    
    console.print(f"[bold cyan]Wordlist Details:[/bold cyan]\n{charset_desc}{length_desc}{prefix_desc}{suffix_desc}{threads_desc}")

if __name__ == "__main__":
    print_banner()

    parser = argparse.ArgumentParser(description="DRC Wordlist Generator")
    parser.add_argument("-c", "--charset", type=str, required=True, help="Character set (e.g., 'abc123!@#')")
    parser.add_argument("-min", "--min_length", type=int, required=True, help="Minimum word length")
    parser.add_argument("-max", "--max_length", type=int, required=True, help="Maximum word length")
    parser.add_argument("-p", "--prefix", type=str, default="", help="Prefix (optional)")
    parser.add_argument("-s", "--suffix", type=str, default="", help="Suffix (optional)")
    parser.add_argument("-o", "--output", type=str, default="wordlist.txt", help="Output file name")
    parser.add_argument("-l", "--limit", type=int, default=0, help="Limit the number of words (0 for no limit)")
    parser.add_argument("-t", "--threads", type=int, default=4, help="Number of threads to use for generation")
    parser.add_argument("--predefined", type=str, choices=['alpha', 'alphanumeric', 'digits', 'special', 'lower', 'upper'],
                        help="Use predefined character set")

    args = parser.parse_args()

    # Get predefined charset if selected
    if args.predefined:
        charset = get_predefined_charset(args.predefined)
        if not charset:
            console.print("[bold red]Error: Invalid predefined charset.[/bold red]")
            exit(1)
    else:
        charset = args.charset

    # Validate inputs before proceeding
    try:
        validate_input(args.min_length, args.max_length, charset)
        print_wordlist_description(charset, args.min_length, args.max_length, args.prefix, args.suffix, args.threads)
        generate_wordlist(charset, args.min_length, args.max_length, args.prefix, args.suffix, args.output, args.limit, args.threads)
    except ValueError as e:
        console.print(f"[bold red]Error: {e}[/bold red]")
