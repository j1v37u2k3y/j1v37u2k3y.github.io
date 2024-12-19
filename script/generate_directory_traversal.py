#!/usr/bin/env python3
import argparse

def generate_traversal_strings(max_depth=10, include_wildcards=True, base_path="../"):
    """
    Generate directory traversal strings up to specified depth.
    Args:
        max_depth (int): Maximum depth of directory traversal
        include_wildcards (bool): Whether to include wildcard patterns
        base_path (str): Base path to use for traversal (default: "../")
    Returns:
        list: List of generated traversal strings
    """
    traversal_strings = []

    # Generate strings for each depth
    for i in range(1, max_depth + 1):
        # Basic traversal string
        traversal = base_path * i
        traversal_strings.append(traversal)

        # Add wildcard version if requested
        if include_wildcards:
            wildcard = traversal + "*"
            traversal_strings.append(wildcard)

    return traversal_strings

def main():
    parser = argparse.ArgumentParser(description='Generate directory traversal strings')
    parser.add_argument('-d', '--depth', type=int, default=10,
                      help='Maximum depth for traversal (default: 10)')
    parser.add_argument('-w', '--wildcards', action='store_true',
                      help='Include wildcard patterns')
    parser.add_argument('-o', '--output', type=str,
                      help='Output file (default: print to stdout)')
    parser.add_argument('-b', '--base', type=str, default="../",
                      help='Base path for traversal (default: "../")')

    args = parser.parse_args()

    # Generate the strings
    traversal_strings = generate_traversal_strings(
        max_depth=args.depth,
        include_wildcards=args.wildcards,
        base_path=args.base
    )

    # Output handling
    if args.output:
        with open(args.output, 'w') as f:
            for string in traversal_strings:
                f.write(string + '\n')
        print(f"Written {len(traversal_strings)} patterns to {args.output}")
    else:
        for string in traversal_strings:
            print(string)

if __name__ == "__main__":
    main()
