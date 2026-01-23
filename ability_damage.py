"""
Item Damage Calculator and Comparison Tool
Compares items with different ability damage and ability scaling values.
Formula: damage = ability_damage * (1 + intelligence * ability_scaling / 100)
"""

import sys

class Item:
    def __init__(self, name, ability_damage, ability_scaling, cooldown=1.0, rarity=None, mana_cost=0):
        """
        Initialize an item with its stats.
        
        Args:
            name: Item name
            ability_damage: Base ability damage
            ability_scaling: Ability scaling percentage (e.g., 0.5 for 0.5%)
            cooldown: Ability cooldown in seconds (default: 1.0)
            rarity: Item rarity (e.g., LEGENDARY, EPIC, RARE, UNCOMMON, COMMON)
            mana_cost: Mana cost per ability (default: 0)
        """
        self.name = name
        self.ability_damage = ability_damage
        self.ability_scaling = ability_scaling
        self.cooldown = cooldown
        self.rarity = rarity
        self.mana_cost = mana_cost
    
    def calculate_damage(self, intelligence):
        """
        Calculate total damage output for given intelligence.
        
        Args:
            intelligence: Intelligence stat value
            
        Returns:
            Total damage output
        """
        return self.ability_damage * (1 + intelligence * self.ability_scaling / 100)
    
    def __str__(self):
        rarity_str = f" [{self.rarity}]" if self.rarity else ""
        return f"{self.name}{rarity_str} (AD: {self.ability_damage}, AS: {self.ability_scaling}%, CD: {self.cooldown}s)"


def compare_items(items, intelligence):
    """
    Compare multiple items at a given intelligence value.
    
    Args:
        items: List of Item objects
        intelligence: Intelligence stat value
    """
    print("=" * 80)
    print("ITEM DAMAGE COMPARISON")
    print("=" * 80)
    print(f"\nFormula: damage = ability_damage * (1 + intelligence * ability_scaling / 100)")
    print("\nItems being compared:")
    for i, item in enumerate(items, 1):
        print(f"  {i}. {item}")
    
    print("\n" + "=" * 130)
    print(f"{'Item Name':<30}{'Damage':<15}{'DPS':<15}{'Mana Cost':<12}{'Dmg/Mana':<15}{'DPS/Mana':<15}{'CD (s)'}")
    print("=" * 130)
    
    damages = []
    for item in items:
        damage = item.calculate_damage(intelligence)
        dps = damage / item.cooldown if item.cooldown > 0 else 0
        dmg_per_mana = damage / item.mana_cost if item.mana_cost > 0 else float('inf')
        dps_per_mana = dps / item.mana_cost if item.mana_cost > 0 else float('inf')
        damages.append((item, damage, dps, dmg_per_mana, dps_per_mana))
        
        mana_str = f"{item.mana_cost:.0f}" if item.mana_cost > 0 else "0"
        dmg_mana_str = f"{dmg_per_mana:.4f}" if dmg_per_mana != float('inf') else "∞"
        dps_mana_str = f"{dps_per_mana:.4f}" if dps_per_mana != float('inf') else "∞"
        print(f"{item.name:<30}{damage:<15.2f}{dps:<15.2f}{mana_str:<12}{dmg_mana_str:<15}{dps_mana_str:<15}{item.cooldown:.2f}")
    
    # Show top 5 by damage, DPS, and damage per mana
    top5_damage = sorted(damages, key=lambda x: x[1], reverse=True)[:5]
    top5_dps = sorted(damages, key=lambda x: x[2], reverse=True)[:5]
    top5_dmg_mana = sorted([d for d in damages if d[0].mana_cost > 0], key=lambda x: x[3], reverse=True)[:5]
    
    print(f"\nTop 5 by Damage:")
    for i, (item, damage, _, _, _) in enumerate(top5_damage, 1):
        print(f"  {i}. {item.name}: {damage:.2f}")
    
    print(f"\nTop 5 by DPS:")
    for i, (item, _, dps, _, _) in enumerate(top5_dps, 1):
        print(f"  {i}. {item.name}: {dps:.2f}")
    
    print(f"\nTop 5 by Damage per Mana:")
    for i, (item, _, _, dmg_mana, _) in enumerate(top5_dmg_mana, 1):
        print(f"  {i}. {item.name}: {dmg_mana:.4f}")
    
    # Mana usage per second analysis
    print(f"\n" + "=" * 130)
    print("MANA USAGE PER SECOND BREAKPOINTS")
    print("=" * 130)
    
    # Calculate mana per second for each item
    mana_per_sec_data = []
    for item, damage, dps, dmg_per_mana, dps_per_mana in damages:
        mana_per_sec = item.mana_cost / item.cooldown if item.cooldown > 0 and item.mana_cost > 0 else 0
        mana_per_sec_data.append((item, damage, dps, mana_per_sec))
    
    # For each breakpoint, show top 3 items by DPS that don't exceed the mana rate
    breakpoints = [50, 100, 150, 200]
    for breakpoint in breakpoints:
        # Filter items that don't exceed the breakpoint
        eligible = [(item, damage, dps, mps) for item, damage, dps, mps in mana_per_sec_data 
                   if mps <= breakpoint and mps > 0]
        # Sort by DPS and take top 3
        top3 = sorted(eligible, key=lambda x: x[2], reverse=True)[:3]
        
        print(f"\nTop 3 by DPS at ≤{breakpoint} Mana/sec:")
        if top3:
            for i, (item, _, dps, mps) in enumerate(top3, 1):
                print(f"  {i}. {item.name}: {dps:.2f} DPS ({mps:.2f} mana/sec)")
        else:
            print(f"  No items found within this mana rate")
    
    print("=" * 130)


def find_breakpoint(item1, item2, intel_range=(0, 1000)):
    """
    Find the intelligence value where two items have equal DPS (breakpoint).
    
    Args:
        item1: First Item object
        item2: Second Item object
        intel_range: Tuple of (min, max) intelligence to search
        
    Returns:
        Intelligence value at breakpoint, or None if no breakpoint exists
    """
    # At breakpoint: ad1*(1+I*as1/100)/cd1 == ad2*(1+I*as2/100)/cd2
    # Let A1 = ad1/cd1, B1 = ad1*as1/(100*cd1); A2 = ad2/cd2, B2 = ad2*as2/(100*cd2)
    # Solve for I: A1 + B1*I = A2 + B2*I  => I = (A1 - A2) / (B2 - B1)
    A1 = item1.ability_damage / item1.cooldown
    B1 = item1.ability_damage * item1.ability_scaling / (100 * item1.cooldown)
    A2 = item2.ability_damage / item2.cooldown
    B2 = item2.ability_damage * item2.ability_scaling / (100 * item2.cooldown)

    denominator = B2 - B1
    if abs(denominator) < 0.0001:  # Essentially parallel scaling in DPS
        return None

    breakpoint = (A1 - A2) / denominator

    if intel_range[0] <= breakpoint <= intel_range[1]:
        return breakpoint
    return None


def detailed_comparison(item1, item2, intel_range=(0, 1000, 50)):
    """
    Detailed comparison between two specific items.
    
    Args:
        item1: First Item object
        item2: Second Item object
        intel_range: Tuple of (start, stop, step) for intelligence values
    """
    print("\n" + "=" * 80)
    print(f"DETAILED COMPARISON: {item1.name} vs {item2.name}")
    print("=" * 80)
    print(f"{item1.name}: AD={item1.ability_damage}, AS={item1.ability_scaling}%, CD={item1.cooldown}s")
    print(f"{item2.name}: AD={item2.ability_damage}, AS={item2.ability_scaling}%, CD={item2.cooldown}s")
    
    # Find breakpoint
    breakpoint = find_breakpoint(item1, item2, (intel_range[0], intel_range[1]))
    if breakpoint:
        print(f"\n⚡ DPS Breakpoint at Intelligence = {breakpoint:.2f}")
        better_below = item1 if (item1.calculate_damage(0) / item1.cooldown) > (item2.calculate_damage(0) / item2.cooldown) else item2
        better_above = item2 if better_below is item1 else item1
        print(f"   Below {breakpoint:.2f}: {better_below.name} is better (DPS)")
        print(f"   Above {breakpoint:.2f}: {better_above.name} is better (DPS)")
    else:
        # Determine which is always better by DPS
        if (item1.calculate_damage(500) / item1.cooldown) > (item2.calculate_damage(500) / item2.cooldown):
            print(f"\n✓ {item1.name} is always better by DPS (no breakpoint)")
        else:
            print(f"\n✓ {item2.name} is always better by DPS (no breakpoint)")
    
    print("\n" + "-" * 110)
    print(f"{'Int':<6}{'Item 1 Dmg':<15}{'Item 1 DPS':<15}{'Item 2 Dmg':<15}{'Item 2 DPS':<15}{'DPS Diff':<12}{'Winner (DPS)'}")
    print("-" * 110)
    
    intelligence_values = range(intel_range[0], intel_range[1] + 1, intel_range[2])
    for intel in intelligence_values:
        dmg1 = item1.calculate_damage(intel)
        dmg2 = item2.calculate_damage(intel)
        dps1 = dmg1 / item1.cooldown if item1.cooldown > 0 else 0
        dps2 = dmg2 / item2.cooldown if item2.cooldown > 0 else 0
        diff = abs(dps1 - dps2)
        winner = item1.name if dps1 > dps2 else item2.name
        print(f"{intel:<6}{dmg1:<15.2f}{dps1:<15.2f}{dmg2:<15.2f}{dps2:<15.2f}{diff:<12.2f}{winner}")
    
    print("=" * 80)


def compare_top_items_by_mana(items, intelligence, cooldown_bonus=0.15):
    """
    Compare the top 5 items by damage and DPS using damage per mana.
    
    Args:
        items: List of Item objects
        intelligence: Intelligence stat value
        cooldown_bonus: Cooldown bonus applied to items
    """
    # Calculate damage and DPS for all items
    results = []
    for item in items:
        damage = item.calculate_damage(intelligence)
        dps = damage / item.cooldown if item.cooldown > 0 else 0
        results.append((item, damage, dps))
    
    # Get top 5 by damage and top 5 by DPS
    top5_damage = sorted(results, key=lambda x: x[1], reverse=True)[:5]
    top5_dps = sorted(results, key=lambda x: x[2], reverse=True)[:5]
    
    # Combine and deduplicate
    top_items_set = set()
    for item, _, _ in top5_damage + top5_dps:
        top_items_set.add(item.name)
    
    top_items = [item for item in items if item.name in top_items_set]
    
    print("\n" + "=" * 120)
    print("TOP ITEMS ANALYSIS - DAMAGE PER MANA")
    print("=" * 120)
    print(f"\nAt Intelligence = {intelligence}:")
    print(f"{'Item Name':<30}{'Damage':<15}{'DPS':<15}{'Mana Cost':<12}{'Dmg/Mana':<15}{'DPS/Mana':<15}{'Status'}")
    print("-" * 120)
    
    # Calculate damage per mana for top items
    mana_results = []
    for item in top_items:
        damage = item.calculate_damage(intelligence)
        dps = damage / item.cooldown if item.cooldown > 0 else 0
        
        if item.mana_cost > 0:
            dmg_per_mana = damage / item.mana_cost
            dps_per_mana = dps / item.mana_cost
            status = "✓"
        else:
            dmg_per_mana = float('inf') if damage > 0 else 0
            dps_per_mana = float('inf') if dps > 0 else 0
            status = "No cost"
        
        mana_results.append((item, damage, dps, dmg_per_mana, dps_per_mana, status))
    
    # Sort by damage per mana
    mana_results.sort(key=lambda x: x[3], reverse=True)
    
    print("=" * 80)


def main():
    """Main function with example items."""
    
    # Parse command-line arguments
    if len(sys.argv) < 2:
        print("Usage: python ability_damage.py <intelligence>")
        print("Example: python ability_damage.py 500")
        sys.exit(1)
    
    try:
        intelligence = int(sys.argv[1])
    except ValueError:
        print("Error: Intelligence must be an integer")
        sys.exit(1)
    
    if intelligence < 0:
        print("Error: Intelligence must be non-negative")
        sys.exit(1)

    cooldown_bonus = 0.15
    if len(sys.argv) >= 3:
        try:
            cooldown_bonus = float(sys.argv[2])
        except ValueError:
            print("Error: Cooldown bonus must be a number")
            sys.exit(1)
        if cooldown_bonus < 0:
            print("Error: Cooldown bonus must be non-negative")
            sys.exit(1)
    
    # Game items with ability damage, scaling values, and cooldowns
    items = [
        Item("Aurora Staff", ability_damage=10000, ability_scaling=0.2, cooldown=1.0, rarity="LEGENDARY", mana_cost=5),
        Item("Aspect Of The Dragons", ability_damage=18000, ability_scaling=0.1, cooldown=0.05, rarity="LEGENDARY", mana_cost=50),
        Item("Bingo Blaster", ability_damage=625, ability_scaling=1, cooldown=1.0, rarity="EPIC", mana_cost=62.5),
        Item("Blast O' Lantern", ability_damage=3000, ability_scaling=0.2, cooldown=0.05, rarity="RARE", mana_cost=75),
        Item("Bonzo's Staff", ability_damage=1000, ability_scaling=0.2, cooldown=0.05, rarity="RARE", mana_cost=45),
        Item("⚚ Bonzo's Staff", ability_damage=1100, ability_scaling=0.2, cooldown=0.05, rarity="RARE", mana_cost=45),
        Item("Celeste Wand", ability_damage=40, ability_scaling=1, cooldown=0.05, rarity="UNCOMMON", mana_cost=35),
        Item("Ember Rod", ability_damage=30, ability_scaling=1, cooldown=30.0, rarity="EPIC", mana_cost=75),
        Item("Fire Fury Staff", ability_damage=42000, ability_scaling=0.3, cooldown=20.0, rarity="EPIC", mana_cost=500),
        Item("Frozen Scythe", ability_damage=1000, ability_scaling=0.3, cooldown=0.05, rarity="RARE", mana_cost=25),
        Item("Giant's Sword", ability_damage=100000, ability_scaling=0.05, cooldown=30.0, rarity="LEGENDARY", mana_cost=50),
        Item("Glacial Scythe", ability_damage=1500, ability_scaling=0.3, cooldown=0.05, rarity="EPIC", mana_cost=37.5),
        Item("Golem Sword", ability_damage=250, ability_scaling=1, cooldown=3.0, rarity="RARE", mana_cost=35),
        Item("Ink Wand", ability_damage=10000, ability_scaling=1, cooldown=30.0, rarity="EPIC", mana_cost=30),
        Item("Jerry-chine Gun", ability_damage=500, ability_scaling=0.2, cooldown=0.05, rarity="EPIC", mana_cost=150),
        Item("Jinxed Voodoo Doll", ability_damage=2222, ability_scaling=1, cooldown=3.0, rarity="EPIC", mana_cost=90),
        Item("Jinxed Voodoo Doll (full)", ability_damage=2222*12, ability_scaling=1, cooldown=3.0*12, rarity="EPIC", mana_cost=90),
        Item("Leaping Sword", ability_damage=350, ability_scaling=1, cooldown=1.0, rarity="EPIC", mana_cost=25),
        Item("Midas Staff", ability_damage=40000, ability_scaling=0.3, cooldown=1.0, rarity="LEGENDARY", mana_cost=250),
        Item("Pigman Sword", ability_damage=30000, ability_scaling=0.1, cooldown=5.0, rarity="LEGENDARY", mana_cost=200),
        Item("Silk-Edge Sword", ability_damage=400, ability_scaling=1, cooldown=1.0, rarity="LEGENDARY", mana_cost=25),
        Item("Skeleton Hat", ability_damage=50, ability_scaling=1, cooldown=0.05, rarity="COMMON", mana_cost=500),
        Item("Spirit Sceptre", ability_damage=2000, ability_scaling=0.2, cooldown=0.05, rarity="LEGENDARY", mana_cost=100),
        Item("⚚ Spirit Sceptre", ability_damage=2250, ability_scaling=0.2, cooldown=0.05, rarity="LEGENDARY", mana_cost=100),
        Item("Staff Of The Volcano", ability_damage=24000, ability_scaling=0.3, cooldown=30.0, rarity="RARE", mana_cost=50),
        Item("Starlight Wand", ability_damage=50, ability_scaling=1, cooldown=2, rarity="RARE", mana_cost=60),
        Item("The Alchemist's Staff", ability_damage=10000, ability_scaling=0.3, cooldown=0.05, rarity="RARE", mana_cost=499999.5),
        Item("Ultimate Wither Scroll", ability_damage=10000, ability_scaling=0.3, cooldown=0.05, rarity="EPIC", mana_cost=150),
        Item("Vampire Witch Mask", ability_damage=3000, ability_scaling=0.2, cooldown=1.0, rarity="EPIC", mana_cost=5000),
        Item("Voodoo Doll", ability_damage=1500, ability_scaling=1, cooldown=5.0, rarity="RARE", mana_cost=100),
        Item("Witch Mask", ability_damage=4000, ability_scaling=1, cooldown=1.0, rarity="RARE", mana_cost=5000),
        Item("Yeti Sword", ability_damage=15000, ability_scaling=0.3, cooldown=1.0, rarity="LEGENDARY", mana_cost=125),
    ]

    # Apply configurable cooldown bonus after items are initialized
    for item in items:
        item.cooldown += cooldown_bonus
    
    # Compare all items
    compare_items(items, intelligence)


if __name__ == "__main__":
    main()
