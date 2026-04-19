import random

class Hammurabi:
    def __init__(self):
        self.rand = random.Random()

    def get_int_input(self, prompt, minimum=0, maximum=None):
        while True:
            try:
                value = int(input(prompt))
                if value < minimum:
                    print(f"Please enter a number greater than or equal to {minimum}.")
                    continue
                if maximum is not None and value > maximum:
                    print(f"Please enter a number less than or equal to {maximum}.")
                    continue
                
                return value
            except ValueError:
                print("Please enter a valid whole number.")

    def get_signed_int_input(self, prompt):
        while True:
            try:
                return int(input(prompt))
            except ValueError:
                print("Please enter a valid whole number.")

    def print_intro(self):
        print("=" * 60)
        print("HAMMURABI")
        print("Try your hand at governing ancient Sumeria for 10 years.")
        print("Each year you must decide how much land to buy or sell,")
        print("how much grain to feed your people, and how many acres to plant.")
        print("=" * 60)
        print()

    def suggest_land_trade(self, population, acres, grain, land_price):
        # Keep enough grain for full feeding and full planting of available workers.
        reserve_for_food = population * 20
        reserve_for_seed = population * 10 * 2
        reserve_total = reserve_for_food + reserve_for_seed
        target_acres = population * 10

        available_for_land = max(0, grain - reserve_total)
        max_buy = available_for_land // land_price

        if acres < target_acres and max_buy > 0:
            return min(target_acres - acres, max_buy)

        if acres > target_acres and grain < reserve_total:
            grain_shortfall = reserve_total - grain
            sell_needed = (grain_shortfall + land_price - 1) // land_price
            return -min(acres - target_acres, sell_needed)

        return 0

    def suggest_planting(self, population, acres, grain):
        no_starvation_feed = population * 20
        grain_after_feed = max(0, grain - no_starvation_feed)
        max_plant_by_land = acres
        max_plant_by_people = population * 10
        max_plant_by_grain = grain_after_feed // 2
        return min(max_plant_by_land, max_plant_by_people, max_plant_by_grain)

    def advisor_menu(self, population, acres, grain, land_price):
        while True:
            print("\nAdvisor menu:")
            print("1. Continue without advice")
            print("2. Ask land advisor")
            print("3. Ask farm advisor")
            print("4. Ask both advisors")

            choice = self.get_int_input("Choose an option (1-4): ", 1, 4)

            if choice == 1:
                return

            if choice in (2, 4):
                trade = self.suggest_land_trade(population, acres, grain, land_price)
                if trade > 0:
                    print(f"Land advisor: buy about {trade} acres this year.")
                elif trade < 0:
                    print(f"Land advisor: sell about {-trade} acres this year.")
                else:
                    print("Land advisor: hold steady this year (buy/sell 0 acres).")

            if choice in (3, 4):
                plant = self.suggest_planting(population, acres, grain)
                print("Farm advisor:")
                print(f"- To avoid starvation, feed about {population * 20} bushels.")
                print(f"- Then plant about {plant} acres (seed cost: {plant * 2} bushels).")

            print()

    def main(self):
        self.playGame()

    def playGame(self):
        self.print_intro()

        year = 1
        population = 100
        acres = 1000
        grain = 2800
        land_price = random.randint(17, 26)

        total_starved = 0
        total_percent_starved = 0
        plague_deaths_total = 0

        while year <= 10:
            print(f"\n{'-' * 60}")
            print(f"Year {year}")
            print(f"{'-' * 60}")
            print(f"Population: {population}")
            print(f"Acres owned: {acres}")
            print(f"Grain in storage: {grain} bushels")
            print(f"Land price: {land_price} bushels per acre")

            self.advisor_menu(population, acres, grain, land_price)

            # Buy or sell land in one prompt.
            while True:
                trade = self.get_signed_int_input(
                    "How many acres do you wish to buy (negative to sell)? "
                )
                if trade > 0 and trade * land_price > grain:
                    print("You do not have enough grain for that.")
                    continue
                if trade < 0 and -trade > acres:
                    print("You do not own that much land.")
                    continue
                break

            if trade >= 0:
                acres += trade
                grain -= trade * land_price
            else:
                sold = -trade
                acres -= sold
                grain += sold * land_price

            # Feed people
            max_feed = grain
            feed = self.get_int_input(
                f"How many bushels do you wish to feed your people? ", 0, max_feed
            )
            grain -= feed

            # Plant crops
            max_plant_by_land = acres
            max_plant_by_grain = grain // 2
            max_plant_by_people = population * 10
            max_plant = min(max_plant_by_land, max_plant_by_grain, max_plant_by_people)

            plant = self.get_int_input(
                f"How many acres do you wish to plant with seed? ", 0, max_plant
            )
            grain -= plant * 2

            # Starvation
            people_fed = feed // 20
            starved = max(0, population - people_fed)

            if population > 0 and (starved / population) > 0.45:
                print("\nYou starved too many people in one year.")
                print("The people have overthrown you.")
                print("Game over.")
                return

            total_starved += starved
            if population > 0:
                total_percent_starved += (starved / population) * 100

            population -= starved

            # Immigration
            immigrants = 0
            if starved == 0:
                immigrants = (20 * acres + grain) // (100 * population) + 1
                population += immigrants

            # Plague
            plague_deaths = 0
            if random.randint(1, 100) <= 15:
                plague_deaths = population // 2
                population -= plague_deaths
                plague_deaths_total += plague_deaths

            # Harvest
            yield_per_acre = random.randint(1, 6)
            harvest = plant * yield_per_acre
            grain += harvest

            # Rats
            rats_ate = 0
            if random.randint(1, 100) <= 40:
                rats_ate = grain // random.choice([2, 3, 4])
                grain -= rats_ate

            # End of year report
            print("\nYear-end report:")
            print(f"{starved} people starved.")
            if immigrants > 0:
                print(f"{immigrants} people came to the city.")
            else:
                print("No new people came to the city.")
            if plague_deaths > 0:
                print(f"A plague killed {plague_deaths} people.")
            print(f"Harvest was {yield_per_acre} bushels per acre.")
            print(f"Total harvest: {harvest} bushels.")
            print(f"Rats ate {rats_ate} bushels.")
            print(f"Population is now {population}.")
            print(f"You now own {acres} acres.")
            print(f"You now have {grain} bushels in storage.")

            year += 1
            land_price = random.randint(17, 26)

            if population <= 0:
                print("\nAll the people are gone. Your reign has ended.")
                return

        # Final evaluation
        avg_starved_percent = total_percent_starved / 10
        acres_per_person = acres // max(population, 1)

        print(f"\n{'=' * 60}")
        print("Your 10-year rule has ended.")
        print(f"{'=' * 60}")
        print(f"Average percentage of people starved per year: {avg_starved_percent:.1f}%")
        print(f"Plague deaths during your rule: {plague_deaths_total}")
        print(f"Acres per person: {acres_per_person}")

        if avg_starved_percent > 33 or acres_per_person < 7:
            print("Your rule was terrible. The kingdom curses your name.")
        elif avg_starved_percent > 10 or acres_per_person < 9:
            print("Your rule was poor. You survived, but barely.")
        elif avg_starved_percent > 3 or acres_per_person < 10:
            print("Your rule was decent. The people are reasonably satisfied.")
        else:
            print("A fantastic performance! You are remembered as a wise ruler.")



  

if __name__ == "__main__":
    hammurabi = Hammurabi()
    hammurabi.main()
