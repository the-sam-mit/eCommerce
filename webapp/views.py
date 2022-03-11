from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.models import User
from django.shortcuts import redirect

from .models import Item, Cart, Cart_Product

def index(request):
    items_list = Item.objects.order_by('item_name')
    template = loader.get_template('webapp/index.html')
    context = {'items_list': items_list}
    return render(request, 'webapp/index.html', context)

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

class ResultsView(generic.DetailView):
    model = Item
    template_name = 'webapp/detail.html'

def add_to_cart(request, product_id):
	print(request.user.id)
	print(request.user.username)
	print(product_id)
	qqty = request.POST.get('qty')
	print("pta chla", qqty)
	cart_exists=Cart.objects.filter(pk=request.user.id).exists()
	user_existing = get_object_or_404(User, pk=request.user.id)

	if qqty != None:
		if cart_exists == False:
			cart_add = Cart(cart_user = user_existing, cart_total='0.0')
			cart_add.save()

		cart_add = Cart.objects.get(cart_user = user_existing)
		print("aao", cart_add)
		qqty = float(qqty)

		product_at_disposal = get_object_or_404(Item, pk=product_id)
		pro_exists = Cart_Product.objects.filter(cart_present = cart_add, cart_product = product_at_disposal).exists()
		if pro_exists == False:
			prod_add = Cart_Product(cart_present = cart_add, cart_product = product_at_disposal, cart_subtotal= product_at_disposal.item_price * qqty, cart_quantity = qqty)
			prod_add.save()
			cart_add.cart_total += prod_add.cart_subtotal
			cart_add.save()
		else:
			prro = get_object_or_404(Cart_Product, cart_present = cart_add, cart_product = product_at_disposal)
			cart_add.cart_total -= prro.cart_subtotal 
			prro.cart_quantity = qqty
			prro.cart_subtotal = qqty*product_at_disposal.item_price
			prro.save()
			cart_add.cart_total += prro.cart_subtotal
			cart_add.save()

		items_list = Cart_Product.objects.filter(cart_present = cart_add)
		print(cart_add.cart_total)
		context = {'items_list': items_list, 'carT': cart_add}
		return render(request, 'webapp/cart.html', context)
	
	else:
		if cart_exists == True:
			cart_add = Cart.objects.get(cart_user = user_existing)
			items_list = Cart_Product.objects.filter(cart_present = cart_add)
			print(items_list)
			context = {'items_list': items_list, 'carT': cart_add}
			return render(request, 'webapp/cart.html', context)
		else:
			return render(request, 'webapp/cart.html')		

def added_cart(request):
	cart_exists=Cart.objects.filter(pk=request.user.id).exists()
	print(cart_exists,'Added cart')
	user_existing = get_object_or_404(User, pk=request.user.id)
	if cart_exists == False:
		cart_add = Cart(cart_user = user_existing, cart_total='0.0')
		cart_add.save()
	cart_add = Cart.objects.get(cart_user = user_existing)
	items_list = Cart_Product.objects.filter(cart_present = cart_add)
	print('Items :', items_list)
	print('Cart_add :', cart_add)
	context = {'items_list': items_list, 'carT': cart_add}
	return render(request, 'webapp/cart.html', context)

def delete_pro(request, delete_id, product_id):
	qqty = get_object_or_404(Cart_Product, id=delete_id)
	qqty = qqty.cart_subtotal
	Cart_Product.objects.filter(id = delete_id).delete()
	cart_exists=Cart.objects.filter(pk=request.user.id).exists()
	print(cart_exists)
	user_existing = get_object_or_404(User, pk=request.user.id)
	if cart_exists == False:
		cart_add = Cart(cart_user = user_existing, cart_total='0.0')
		cart_add.save()
	cart_add = Cart.objects.get(cart_user = user_existing)
	if cart_exists == True:
		cart_add.cart_total -= qqty
		cart_add.save()
	items_list = Cart_Product.objects.filter(cart_present = cart_add)
	context = {'items_list': items_list, 'carT': cart_add}
	return redirect(request.META['HTTP_REFERER'])

def deleted_p(request, delete_id):
	qqty = get_object_or_404(Cart_Product, id=delete_id)
	qqty = qqty.cart_subtotal
	Cart_Product.objects.filter(id = delete_id).delete()
	cart_exists=Cart.objects.filter(pk=request.user.id).exists()
	print(cart_exists)
	user_existing = get_object_or_404(User, pk=request.user.id)
	if cart_exists == False:
		cart_add = Cart(cart_user = user_existing, cart_total='0.0')
		cart_add.save()
	cart_add = Cart.objects.get(cart_user = user_existing)
	if cart_exists == True:
		cart_add.cart_total -= qqty
		cart_add.save()
	items_list = Cart_Product.objects.filter(cart_present = cart_add)
	context = {'items_list': items_list, 'carT': cart_add}
	return redirect(request.META['HTTP_REFERER'])

def Apriori(items_list):
	# Implement Apriori here
	print('Apriori', items_list)

def order_it(request):
	# here cart_id must also be returned
	cart_exists=Cart.objects.filter(pk=request.user.id).exists()
	print(cart_exists,'Added cart')
	user_existing = get_object_or_404(User, pk=request.user.id)
	if cart_exists == False:
		cart_add = Cart(cart_user = user_existing, cart_total='0.0')
		cart_add.save()
	cart_add = Cart.objects.get(cart_user = user_existing)
	items_list = Cart_Product.objects.filter(cart_present = cart_add)
	print('Items :', items_list)
	print('Cart_add :', cart_add)
	Apriori(items_list)
	return render(request, 'webapp/order.html')

def add_order(request):
	# add here db entry for current order 
	fname = request.POST.get('firstname')
	address = request.POST.get('address')
	city = request.POST.get('city')
	state = request.POST.get('state')
	pincode = request.POST.get('zip')
	user_existing = get_object_or_404(User, pk=request.user.id)
	cart_add = Cart.objects.get(cart_user = user_existing)

	context = {'fname': fname, 'address': address, 'city': city, 'state': state, 'pincode': pincode, 'amt':cart_add.cart_total}
	
	# ALL order details in the rendered page, below is temporary
	return render(request, 'webapp/invoice.html', context)

