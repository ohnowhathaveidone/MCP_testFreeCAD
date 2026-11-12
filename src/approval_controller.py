def request_user_approval(proposals: list[dict]) -> bool:
    """
    Displays proposed changes in the terminal and asks the user for confirmation.
    Future-proof: Can be replaced later with a GUI modal dialog returning True/False.
    """
    if not proposals:
        print("\n[Notice] No name changes were proposed by the agent.")
        return False

    print("\n" + "="*50)
    print("PROPOSED CAD MODEL CHANGES:")
    print("="*50)
    for idx, p in enumerate(proposals, 1):
        print(f"{idx}. {p.get('old_name')}  ──>  {p.get('new_name')}")
        print(f"   Reason: {p.get('reasoning')}")
    print("="*50)

    choice = input("\nDo you accept and apply these changes to the FreeCAD model? (y/n): ").strip().lower()
    return choice == 'y'
