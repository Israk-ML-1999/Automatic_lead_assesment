# Generates 25 synthetic leads if needed
from pathlib import Path
import pandas as pd

def ensure_sample(path: str = "data/leads.csv", rows: int = 25):
    p = Path(path)
    if p.exists():
        return
    p.parent.mkdir(parents=True, exist_ok=True)

    first_names = ["Aisha","Jamal","Sara","Liam","Meera","Omar","Emily","Noah","Amina","Hasan",
                   "Nadia","Yusuf","Olivia","Arif","Priya","Zara","Arman","Sophia","Ibrahim","Fatima",
                   "Rafi","Israt","Jason","Maya","Ethan"]
    last_names = ["Rahman","Uddin","Ahmed","Chen","Patel","Faruk","Zhao","Khan","Siddique","Karim",
                  "Rahim","Ali","Park","Chowdhury","Das","Noor","Hossain","Lee","Akter","Chowdhury",
                  "Hasan","Jahan","Roy","Singh","Cole"]
    companies = ["NovaSoft","GreenGrid","Finlytics","EduPro","HealthHub","RetailX","CloudForge","PayFlex",
                 "AgriNext","MediCore","TravelLite","BuildMate","ShopZen","LogiChain","SmartCity",
                 "QuantumBI","MetroBank","FoodFlow","BuildOps","MedAssist","EduNext","TransRoute",
                 "Insurely","Farmlytics","NeoCloud"]
    titles = ["CTO","Ops Manager","Head of Data","VP Engineering","Product Manager","IT Director",
              "DevOps Lead","Engineering Manager","COO","CTO","Head of Ops","CIO","Growth Lead","Head of IT",
              "Program Manager","Data Lead","VP Ops","Ops Director","CTO","Head of Product","Dean Tech",
              "Ops Lead","CISO","Head of Data","Platform Lead"]
    notes_list = [
        "Scaling platform team; exploring automation.",
        "Manual workflows cause delays.",
        "Data pipeline reliability focus.",
        "Wants faster release cycles.",
        "Evaluating vendor options.",
        "Legacy systems migration.",
        "Seeking CI/CD improvements.",
        "Wants observability tooling.",
        "Expansion in SE Asia.",
        "Compliance-heavy workflows.",
        "Seasonal spikes.",
        "Field coordination issues.",
        "Cart abandonment focus.",
        "Routing optimization.",
        "RFP soon; budget tight.",
        "BI refresh planned.",
        "Risk-controlled automation.",
        "SKU complexity.",
        "Ok with pilots.",
        "Clinical workflows.",
        "Budget approval pending.",
        "Dispatch efficiency.",
        "Security automation.",
        "Sensing + analytics.",
        "K8s cost control."
    ]

    rows_out = []
    for i in range(rows):
        fn = first_names[i % len(first_names)]
        ln = last_names[i % len(last_names)]
        comp = companies[i % len(companies)]
        title = titles[i % len(titles)]
        notes = notes_list[i % len(notes_list)]
        email = f"{fn.lower()}.{ln.lower()}@example.com"
        linkedin = f"https://www.linkedin.com/in/{fn.lower()}{ln.lower()}"
        rows_out.append({
            "first_name": fn,
            "last_name": ln,
            "email": email,
            "company": comp,
            "job_title": title,
            "linkedin_url": linkedin,
            "notes": notes
        })
    pd.DataFrame(rows_out).to_csv(p, index=False)
    print(f"Created {path} with {rows} rows")

if __name__ == "__main__":
    ensure_sample()
