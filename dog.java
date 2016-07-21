

package dog

class Dog {
	String name = "Fido";
	void bark(){
		System.out.println("WOOF!");
	}
}


class DogTest {
	public static void main (String[] args){
		Dog dog1;
		dog1.name = "Max";
		dog1.bark();
	}
	
	
	
}