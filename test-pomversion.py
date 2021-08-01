import pomversion

print("pomversion.load()")
try:
    print(f"  => {pomversion.load()}")
except Exception as err:
    print(f"  => {type(err).__name__}{err.args}")

print("---")
print('pomversion.load("pom.xml")')
try:
    print(f"  => {pomversion.load('pom.xml')}")
except Exception as err:
    print(f"  => {type(err).__name__}{err.args}")

print("---")
print("pomversion.load(file)")
with open("pom.xml", "r") as file:
    try:
        print(f"  => {pomversion.load(file)}")
    except Exception as err:
        print(f"  => {type(err).__name__}{err.args}")

print("---")
print("pomversion.from_xml(xml)")
with open("pom.xml", "r") as file:
    try:
        print(f"  => {pomversion.from_xml(file.read())}")
    except Exception as err:
        print(f"  => {type(err).__name__}{err.args}")

print("---")
print('pomversion.load("invalid-version-pom.xml")')
try:
    print(f"  => {pomversion.load('invalid-version-pom.xml')}")
except Exception as err:
    print(f"  => {type(err).__name__}{err.args}")

print("---")
print('pomversion.load(invalid_version_file)')
with open("invalid-version-pom.xml", "r") as file:
    try:
        print(f"  => {pomversion.load(file)}")
    except Exception as err:
        print(f"  => {type(err).__name__}{err.args}")

print("---")
print('pomversion.from_xml(invalid_version_xml)')
with open("invalid-version-pom.xml", "r") as file:
    try:
        print(f"  => {pomversion.from_xml(file.read())}")
    except Exception as err:
        print(f"  => {type(err).__name__}{err.args}")

print("---")
print('pomversion.load("missing-version-pom.xml")')
try:
    print(f"  => {pomversion.load('missing-version-pom.xml')}")
except Exception as err:
    print(f"  => {type(err).__name__}{err.args}")

print("---")
print('pomversion.load(missing_version_file)')
with open("missing-version-pom.xml", "r") as file:
    try:
        print(f"  => {pomversion.load(file)}")
    except Exception as err:
        print(f"  => {type(err).__name__}{err.args}")

print("---")
print('pomversion.from_xml(missing_version_xml)')
with open("missing-version-pom.xml", "r") as file:
    try:
        print(f"  => {pomversion.from_xml(file.read())}")
    except Exception as err:
        print(f"  => {type(err).__name__}{err.args}")

print("---")
print('pomversion.load("no-such-pom.xml")')
try:
    print(f"  => {pomversion.load('no-such-pom.xml')}")
except Exception as err:
    print(f"  => {type(err).__name__}{err.args}")
